#!/usr/bin/env python3
"""
Skill Copier - 從 skills 資料庫複製 skills 到各 IDE 的 skills 目錄

使用方式:
    link-skills [config_file]
    uv run link-skills [config_file]
    python link_skills.py [config_file]

預設 config 檔案: ./skills_config.toml
"""

import shutil
import sys
import tomllib
from pathlib import Path
from typing import Any


def find_skill_in_sources(skill_name: str, source_dirs: list[Path]) -> Path | None:
    """
    在多個 source 目錄中搜尋 skill

    Args:
        skill_name: skill 名稱
        source_dirs: source 目錄列表

    Returns:
        找到的 skill 路徑，找不到則返回 None
    """
    for source_dir in source_dirs:
        skill_path = source_dir / skill_name
        if skill_path.exists() and skill_path.is_dir():
            return skill_path
    return None


def expand_path(path_str: str, config_dir: Path) -> Path:
    """
    展開路徑，支援:
    - ~ (home directory)
    - 相對路徑 (相對於 config 檔案所在目錄)
    """
    path = Path(path_str).expanduser()

    # 如果是相對路徑，相對於 config 檔案所在目錄
    if not path.is_absolute():
        path = (config_dir / path).resolve()

    return path


def load_config(config_path: Path) -> dict[str, Any]:
    """讀取 TOML config 檔案"""
    try:
        with open(config_path, "rb") as f:
            config = tomllib.load(f)
        return config
    except FileNotFoundError:
        print(f"錯誤: Config 檔案不存在: {config_path}")
        sys.exit(1)
    except tomllib.TOMLDecodeError as e:
        print(f"錯誤: Config 檔案格式錯誤: {e}")
        sys.exit(1)


def copy_skill(source: Path, target: Path, dry_run: bool = False) -> bool:
    """
    複製 skill 目錄

    Args:
        source: skill 來源目錄
        target: 目標路徑 (完整路徑，包含 skill 名稱)
        dry_run: 只顯示操作，不實際執行

    Returns:
        是否成功複製
    """
    # 檢查 source 是否存在
    if not source.exists():
        print(f"  ⚠️  來源不存在，跳過: {source}")
        return False

    # 如果 target 已存在
    if target.exists():
        if dry_run:
            print(f"  🔄 將覆蓋: {target}")
        else:
            # 移除已存在的目錄或檔案
            if target.is_file():
                target.unlink()
                print(f"  🗑️  已移除舊檔案: {target}")
            elif target.is_dir():
                shutil.rmtree(target)
                print(f"  🗑️  已移除舊目錄: {target}")

    # 複製目錄
    if dry_run:
        print(f"  ➡️  {source} -> {target}")
    else:
        try:
            shutil.copytree(source, target)
            print(f"  ✅ 已複製: {target.name} <- {source}")
            return True
        except Exception as e:
            print(f"  ❌ 複製失敗: {e}")
            return False

    return True


def link_skills(config_path: Path, dry_run: bool = False):
    """
    主要執行函式：根據 config 複製 skills

    Config 格式：
    - skills: skill 名稱列表 (例如：["architect", "frontend-design"])
    - sources.paths: skill 來源目錄列表 (例如：["./skills", "~/external-skills"])
    - targets: 目標 IDE 目錄設定
    """
    print(f"📖 讀取 config: {config_path}\n")
    config = load_config(config_path)
    config_dir = config_path.parent

    # 解析 skills
    skills_config = config.get("skills", [])

    # 檢查 skills 格式
    if not isinstance(skills_config, list) or not skills_config:
        print("⚠️  Config 中沒有定義任何 skills")
        return

    if not isinstance(skills_config[0], str):
        print("❌ 錯誤：skills 必須是字串列表")
        print("   正確格式：skills = [\"skill1\", \"skill2\"]")
        return

    skill_names = skills_config

    # 解析 sources
    sources_config = config.get("sources", {})
    source_paths_str = sources_config.get("paths", [])

    if not source_paths_str:
        print("⚠️  Config 中沒有定義 sources.paths")
        return

    # 展開 source 路徑
    source_dirs = [expand_path(path, config_dir) for path in source_paths_str]

    print(f"📚 找到 {len(source_dirs)} 個 source 目錄")
    print(f"🎯 找到 {len(skill_names)} 個 skills\n")

    # 建立 skills 列表（帶有實際路徑）
    skills = []
    for skill_name in skill_names:
        skill_path = find_skill_in_sources(skill_name, source_dirs)
        if skill_path:
            skills.append({"name": skill_name, "path": skill_path})
        else:
            print(f"⚠️  找不到 skill: {skill_name}")

    if not skills:
        print("⚠️  沒有可連結的 skills")
        return

    # 解析 targets
    targets = config.get("targets", {})
    if not targets:
        print("⚠️  Config 中沒有定義任何 targets")
        return

    enabled_targets = {
        name: target_config
        for name, target_config in targets.items()
        if target_config.get("enabled", False)
    }

    if not enabled_targets:
        print("⚠️  沒有啟用的 targets (enabled = true)")
        return

    print(f"📍 啟用的 targets: {', '.join(enabled_targets.keys())}\n")

    if dry_run:
        print("🔍 Dry-run 模式 (不會實際複製檔案)\n")

    # 對每個 enabled target 建立連結
    for target_name, target_config in enabled_targets.items():
        print(f"🎯 處理 target: {target_name}")

        target_base_dir = expand_path(target_config["path"], config_dir)
        print(f"   目標目錄: {target_base_dir}")

        # 建立目標目錄 (如果不存在)
        if not target_base_dir.exists():
            if dry_run:
                print(f"   📁 將建立目錄: {target_base_dir}")
            else:
                target_base_dir.mkdir(parents=True, exist_ok=True)
                print(f"   📁 已建立目錄: {target_base_dir}")

        # 收集所有應該存在的 skill 名稱
        expected_skills = {skill["name"] for skill in skills}

        # 檢查並清理不在 config 中的舊項目
        if target_base_dir.exists():
            for item in target_base_dir.iterdir():
                if item.name not in expected_skills:
                    # 這個項目不在 config 中，應該移除
                    if dry_run:
                        print(f"   🗑️  將移除 (不在 config 中): {item.name}")
                    else:
                        if item.is_symlink():
                            item.unlink()
                            print(f"   🗑️  已移除 symlink (不在 config 中): {item.name}")
                        elif item.is_file():
                            item.unlink()
                            print(f"   🗑️  已移除 (不在 config 中): {item.name}")
                        elif item.is_dir():
                            shutil.rmtree(item)
                            print(f"   🗑️  已移除 (不在 config 中): {item.name}")

        # 為每個 skill 複製或更新目錄
        success_count = 0
        kept_count = 0
        updated_count = 0

        for skill in skills:
            skill_name = skill["name"]
            skill_source = skill["path"]
            skill_target = target_base_dir / skill_name

            # 檢查 source 是否存在
            if not skill_source.exists():
                print(f"  ⚠️  來源不存在，跳過: {skill_source}")
                continue

            # 如果 target 已存在
            if skill_target.exists():
                # 目錄已存在，需要更新
                if dry_run:
                    print(f"  🔄 將更新: {skill_name}")
                else:
                    # 移除舊目錄並重新複製
                    if skill_target.is_symlink():
                        skill_target.unlink()
                    elif skill_target.is_file():
                        skill_target.unlink()
                    elif skill_target.is_dir():
                        shutil.rmtree(skill_target)
                    print(f"  🔄 更新: {skill_name}")
                    updated_count += 1

            # 複製目錄
            if not skill_target.exists() or dry_run:
                if dry_run:
                    print(f"  ➕ 將複製: {skill_name} <- {skill_source}")
                    success_count += 1
                else:
                    try:
                        shutil.copytree(skill_source, skill_target)
                        print(f"  ✅ 已複製: {skill_name} <- {skill_source}")
                        success_count += 1
                    except Exception as e:
                        print(f"  ❌ 複製失敗: {e}")

        # 顯示統計
        if dry_run:
            print(
                f"   ✨ 預計: 更新/複製 {success_count - kept_count}，共 {success_count}/{len(skills)} 個 skills\n"
            )
        else:
            print(
                f"   ✨ 完成: 更新/複製 {success_count - kept_count}，共 {success_count}/{len(skills)} 個 skills\n"
            )

    if dry_run:
        print("\n💡 這是 dry-run 模式的結果")
        print("   要實際複製檔案，請執行: ./link_skills.py")
    else:
        print("\n✨ 所有 skills 已複製完成!")


def main():
    """主程式入口"""
    import argparse

    parser = argparse.ArgumentParser(
        description="從 skills 資料庫複製 skills 到各 IDE 的 skills 目錄"
    )
    parser.add_argument(
        "config",
        nargs="?",
        default="skills_config.toml",
        help="Config 檔案路徑 (預設: skills_config.toml)",
    )
    parser.add_argument(
        "-n",
        "--dry-run",
        action="store_true",
        help="Dry-run 模式：只顯示將執行的操作，不實際複製檔案",
    )

    args = parser.parse_args()

    config_path = Path(args.config)
    link_skills(config_path, args.dry_run)


if __name__ == "__main__":
    main()
