# -*- coding: utf-8 -*-
"""
技能自动更新 (Skill Auto-Updater)
---------------------------------
从 GitHub 仓库 greenhushaoqi-lang/stoc 同步最新 skills 到本地 ~/.claude/skills。
- 首次: 浅克隆; 之后: git pull (轻量)
- 按内容哈希检测变化, 只复制 新增/变更 的技能, 报告 新增/更新/移除
- 写同步报告到 reports/skill_sync_YYYYMMDD.md

用法: python update_skills.py
说明: 移除的技能默认只报告不删除(安全), 传 --prune 才会删除本地多余技能。
"""
import os, sys, subprocess, shutil, hashlib, json, datetime as dt

REPO = "https://github.com/greenhushaoqi-lang/stoc.git"
HOME = os.path.expanduser("~")
CLONE = os.path.join(HOME, ".claude", "stoc-skills-repo")
DEST = os.path.join(HOME, ".claude", "skills")
HERE = os.path.dirname(os.path.abspath(__file__))
MANIFEST = os.path.join(HERE, "skills_manifest.json")
PRUNE = "--prune" in sys.argv


def run(cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def sync_repo():
    """确保本地有最新仓库副本。返回 True/False。"""
    if os.path.isdir(os.path.join(CLONE, ".git")):
        r = run(["git", "-C", CLONE, "pull", "--ff-only", "--depth", "1"])
        if r.returncode != 0:                      # pull 失败则重置
            run(["git", "-C", CLONE, "fetch", "--depth", "1", "origin"])
            run(["git", "-C", CLONE, "reset", "--hard", "origin/HEAD"])
        return True
    os.makedirs(os.path.dirname(CLONE), exist_ok=True)
    r = run(["git", "clone", "--depth", "1", REPO, CLONE])
    return r.returncode == 0


def dir_hash(path):
    """技能目录内容哈希(文件相对路径+内容)。"""
    h = hashlib.sha256()
    for root, _, files in os.walk(path):
        for fn in sorted(files):
            fp = os.path.join(root, fn)
            rel = os.path.relpath(fp, path).replace("\\", "/")
            h.update(rel.encode())
            try:
                with open(fp, "rb") as f:
                    h.update(f.read())
            except Exception:
                pass
    return h.hexdigest()


def repo_skill_dirs():
    """仓库内全部技能目录: skills/* (非隐藏) + skills/.system/*。返回 {名称: 源路径}。"""
    base = os.path.join(CLONE, "skills")
    out = {}
    if not os.path.isdir(base):
        return out
    for name in os.listdir(base):
        p = os.path.join(base, name)
        if not os.path.isdir(p):
            continue
        if name == ".system":
            for sub in os.listdir(p):
                sp = os.path.join(p, sub)
                if os.path.isdir(sp):
                    out[sub] = sp
        elif not name.startswith("."):
            out[name] = p
    return out


# 仓库里缺 YAML frontmatter 的技能 -> 同步后自愈补回(否则每天同步都被打回, 无法触发)
LOCAL_PATCHES = {
    "analyze-issue": ("analyze-issue",
        "Triage a GitHub issue for the ZhuLinsen/daily_stock_analysis repo - judge validity, "
        "priority, repo-responsibility scope, difficulty, and recommended action, then write an "
        "analysis doc. Use when asked to analyze or triage a GitHub issue, run /analyze-issue, or "
        "assess whether an issue 是否成立/优先级/是否好解决."),
    "analyze-pr": ("analyze-pr",
        "Review a GitHub Pull Request for the ZhuLinsen/daily_stock_analysis repo - assess necessity, "
        "description completeness, CI/diff verification evidence, compatibility/risk, and whether it "
        "can be merged, then write a review doc. Use when asked to analyze or review a GitHub PR, run "
        "/analyze-pr, or evaluate 是否可直接合入."),
    "fix-issue": ("fix-issue",
        "Implement a fix for a GitHub issue in the ZhuLinsen/daily_stock_analysis repo based on prior "
        "issue analysis, then add verification, risk, and rollback notes per repo rules. Use when "
        "asked to fix or resolve a GitHub issue, run /fix-issue, or implement a bug fix after /analyze-issue."),
}


def apply_local_patches():
    """同步后确保指定技能含 frontmatter(缺则补回)。返回被修复的技能名列表。"""
    fixed = []
    for name, (slug, desc) in LOCAL_PATCHES.items():
        fp = os.path.join(DEST, name, "SKILL.md")
        if not os.path.isfile(fp):
            continue
        try:
            with open(fp, "r", encoding="utf-8") as f:
                body = f.read()
        except Exception:
            continue
        if body.lstrip().startswith("---"):
            continue                                   # 已有 frontmatter, 跳过
        fm = f"---\nname: {slug}\ndescription: {desc}\n---\n\n"
        with open(fp, "w", encoding="utf-8") as f:
            f.write(fm + body)
        fixed.append(name)
    return fixed


def main():
    today = dt.date.today()
    log = []
    ok = sync_repo()
    if not ok:
        print("[失败] 无法获取仓库");
    src = repo_skill_dirs()
    manifest = {}
    if os.path.exists(MANIFEST):
        try: manifest = json.load(open(MANIFEST, encoding="utf-8"))
        except Exception: manifest = {}

    added, updated, unchanged = [], [], []
    new_manifest = {}
    for name, spath in src.items():
        h = dir_hash(spath)
        new_manifest[name] = h
        dpath = os.path.join(DEST, name)
        if not os.path.isdir(dpath):
            shutil.copytree(spath, dpath); added.append(name)
        elif manifest.get(name) != h:
            shutil.rmtree(dpath); shutil.copytree(spath, dpath); updated.append(name)
        else:
            unchanged.append(name)

    # 本地有、仓库已无 -> 移除候选
    local = {d for d in os.listdir(DEST) if os.path.isdir(os.path.join(DEST, d))}
    removed_in_repo = sorted(local - set(src.keys()))
    pruned = []
    if PRUNE:
        for name in removed_in_repo:
            shutil.rmtree(os.path.join(DEST, name)); pruned.append(name)

    patched = apply_local_patches()      # 自愈: 给仓库缺 frontmatter 的技能补回

    json.dump(new_manifest, open(MANIFEST, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    # 报告
    L = [f"# 技能同步报告 {today.isoformat()}", "",
         f"- 仓库: {REPO}",
         f"- 仓库技能总数: **{len(src)}**  本地: **{len(local)}**",
         f"- 新增: **{len(added)}**  更新: **{len(updated)}**  未变: **{len(unchanged)}**",
         f"- 仓库已移除(本地仍存): **{len(removed_in_repo)}**  (本次删除: {len(pruned)})", ""]
    if patched: L.append("**自愈补frontmatter**: " + ", ".join(sorted(patched)))
    if added:   L.append("**新增**: " + ", ".join(sorted(added)))
    if updated: L.append("**更新**: " + ", ".join(sorted(updated)))
    if removed_in_repo:
        L.append(("**已删除**: " if PRUNE else "**仓库已移除(未删, 加 --prune 删)**: ")
                 + ", ".join(removed_in_repo))
    report = "\n".join(L)
    print(report)
    out_dir = os.path.join(HERE, "reports"); os.makedirs(out_dir, exist_ok=True)
    open(os.path.join(out_dir, f"skill_sync_{today.strftime('%Y%m%d')}.md"),
         "w", encoding="utf-8").write(report)


if __name__ == "__main__":
    main()
