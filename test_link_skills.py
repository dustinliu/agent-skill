#!/usr/bin/env python3
"""
Tests for link_skills.py

⚠️  注意：這些測試是在程式碼完成後才寫的，不是真正的 TDD。
真正的 TDD 應該先寫測試，看著它失敗，然後寫最少的程式碼讓它通過。
"""

from pathlib import Path

import pytest

from link_skills import (
    copy_skill,
    expand_path,
    find_skill_in_sources,
    link_skills,
    load_config,
)


class TestFindSkillInSources:
    """測試在多個 sources 中搜尋 skill"""

    def test_finds_skill_in_first_source(self, tmp_path):
        """應該在第一個 source 中找到 skill"""
        # 建立 sources
        source1 = tmp_path / "source1"
        source1.mkdir()
        (source1 / "architect").mkdir()

        source2 = tmp_path / "source2"
        source2.mkdir()

        sources = [source1, source2]

        # 搜尋 skill
        result = find_skill_in_sources("architect", sources)

        # 應該找到第一個 source 中的 skill
        assert result == source1 / "architect"

    def test_finds_skill_in_second_source_if_not_in_first(self, tmp_path):
        """當第一個 source 沒有時，應該在第二個 source 中找到"""
        source1 = tmp_path / "source1"
        source1.mkdir()

        source2 = tmp_path / "source2"
        source2.mkdir()
        (source2 / "frontend-design").mkdir()

        sources = [source1, source2]

        result = find_skill_in_sources("frontend-design", sources)

        assert result == source2 / "frontend-design"

    def test_returns_none_when_skill_not_found(self, tmp_path):
        """當所有 sources 都找不到時，應該返回 None"""
        source1 = tmp_path / "source1"
        source1.mkdir()

        source2 = tmp_path / "source2"
        source2.mkdir()

        sources = [source1, source2]

        result = find_skill_in_sources("nonexistent-skill", sources)

        assert result is None

    def test_handles_empty_sources_list(self, tmp_path):
        """處理空的 sources 列表"""
        result = find_skill_in_sources("any-skill", [])
        assert result is None


class TestExpandPath:
    """測試路徑展開功能"""

    def test_expands_home_directory(self, tmp_path):
        """展開 ~ 為 home directory"""
        config_dir = tmp_path
        result = expand_path("~/test", config_dir)
        assert result == Path.home() / "test"

    def test_resolves_relative_path(self, tmp_path):
        """相對路徑相對於 config 目錄"""
        config_dir = tmp_path
        result = expand_path("./skills/test", config_dir)
        assert result == (config_dir / "skills/test").resolve()

    def test_preserves_absolute_path(self, tmp_path):
        """絕對路徑保持不變"""
        config_dir = tmp_path
        abs_path = "/absolute/path/to/skill"
        result = expand_path(abs_path, config_dir)
        assert result == Path(abs_path)

    def test_combines_relative_path_with_config_dir(self, tmp_path):
        """相對路徑正確結合 config 目錄"""
        config_dir = tmp_path / "configs"
        config_dir.mkdir()
        result = expand_path("../skills", config_dir)
        expected = (config_dir / "../skills").resolve()
        assert result == expected


class TestLoadConfig:
    """測試 config 載入功能"""

    def test_loads_valid_toml_config(self, tmp_path):
        """載入有效的 TOML config"""
        config_file = tmp_path / "test.toml"
        config_file.write_text("""
skills = ["test-skill"]

[sources]
paths = ["./skills"]

[targets.test]
path = "~/.test/skills"
enabled = true
""")

        config = load_config(config_file)

        assert len(config["skills"]) == 1
        assert config["skills"][0] == "test-skill"
        assert "sources" in config
        assert "targets" in config
        assert config["targets"]["test"]["enabled"] is True

    def test_raises_error_on_missing_file(self, tmp_path):
        """不存在的檔案應該結束程式"""
        missing_file = tmp_path / "nonexistent.toml"
        with pytest.raises(SystemExit):
            load_config(missing_file)

    def test_raises_error_on_invalid_toml(self, tmp_path):
        """無效的 TOML 格式應該結束程式"""
        config_file = tmp_path / "invalid.toml"
        config_file.write_text("this is not valid toml {{{")

        with pytest.raises(SystemExit):
            load_config(config_file)


class TestCopySkill:
    """測試 skill 複製功能"""

    def test_copies_skill_successfully(self, tmp_path):
        """成功複製 skill 目錄"""
        source = tmp_path / "source_skill"
        source.mkdir()
        (source / "SKILL.md").write_text("test")

        target_dir = tmp_path / "target"
        target_dir.mkdir()
        target = target_dir / "source_skill"

        result = copy_skill(source, target, dry_run=False)

        assert result is True
        assert target.exists()
        assert target.is_dir()
        assert (target / "SKILL.md").read_text() == "test"

    def test_skips_nonexistent_source(self, tmp_path, capsys):
        """來源不存在時應該跳過"""
        source = tmp_path / "nonexistent"
        target = tmp_path / "target"

        result = copy_skill(source, target, dry_run=False)

        assert result is False
        captured = capsys.readouterr()
        assert "來源不存在" in captured.out

    def test_overwrites_existing_directory(self, tmp_path):
        """覆蓋已存在的目錄"""
        old_source = tmp_path / "old_skill"
        old_source.mkdir()
        (old_source / "old.md").write_text("old content")

        new_source = tmp_path / "new_skill"
        new_source.mkdir()
        (new_source / "new.md").write_text("new content")

        target_dir = tmp_path / "target"
        target_dir.mkdir()
        target = target_dir / "skill"

        # 先複製舊的目錄
        copy_skill(old_source, target, dry_run=False)
        assert (target / "old.md").exists()

        # 覆蓋為新的目錄
        result = copy_skill(new_source, target, dry_run=False)

        assert result is True
        assert target.is_dir()
        assert (target / "new.md").read_text() == "new content"
        assert not (target / "old.md").exists()

    def test_overwrites_existing_file(self, tmp_path):
        """覆蓋已存在的檔案"""
        source = tmp_path / "source_skill"
        source.mkdir()
        (source / "SKILL.md").write_text("content")

        target = tmp_path / "target" / "skill"
        target.parent.mkdir(parents=True)
        target.write_text("this is a file")

        result = copy_skill(source, target, dry_run=False)

        assert result is True
        assert target.is_dir()
        assert (target / "SKILL.md").read_text() == "content"

    def test_dry_run_does_not_copy(self, tmp_path, capsys):
        """Dry-run 模式不實際複製檔案"""
        source = tmp_path / "source_skill"
        source.mkdir()

        target_dir = tmp_path / "target"
        target_dir.mkdir()
        target = target_dir / "source_skill"

        result = copy_skill(source, target, dry_run=True)

        assert result is True
        assert not target.exists()  # 不應該複製
        captured = capsys.readouterr()
        assert "➡️" in captured.out  # 應該顯示將執行的操作


class TestLinkSkills:
    """測試完整的 link skills 流程"""

    def test_links_skills_using_sources_config(self, tmp_path, capsys):
        """使用新的 sources config 格式複製 skills"""
        # 建立多個 source 目錄
        source1 = tmp_path / "source1"
        source1.mkdir()
        (source1 / "architect").mkdir()
        (source1 / "architect" / "SKILL.md").write_text("architect skill")

        source2 = tmp_path / "source2"
        source2.mkdir()
        (source2 / "frontend-design").mkdir()
        (source2 / "frontend-design" / "SKILL.md").write_text("frontend skill")

        # 建立新格式的 config
        config_file = tmp_path / "test.toml"
        config_file.write_text(f"""
skills = ["architect", "frontend-design"]

[sources]
paths = [
    "{source1}",
    "{source2}",
]

[targets.ide]
path = "{tmp_path / "ide" / "skills"}"
enabled = true
""")

        # 執行複製
        link_skills(config_file, dry_run=False)

        # 驗證：兩個 skills 都應該被複製
        ide_skills = tmp_path / "ide" / "skills"
        assert (ide_skills / "architect").is_dir()
        assert (ide_skills / "frontend-design").is_dir()
        architect_content = (ide_skills / "architect" / "SKILL.md").read_text()
        assert architect_content == "architect skill"
        frontend_content = (
            ide_skills / "frontend-design" / "SKILL.md"
        ).read_text()
        assert frontend_content == "frontend skill"

    def test_warns_when_skill_not_found_in_sources(self, tmp_path, capsys):
        """當 skill 在所有 sources 中都找不到時，應該顯示警告"""
        source = tmp_path / "source"
        source.mkdir()

        config_file = tmp_path / "test.toml"
        config_file.write_text(f"""
skills = ["nonexistent-skill"]

[sources]
paths = ["{source}"]

[targets.ide]
path = "{tmp_path / "ide" / "skills"}"
enabled = true
""")

        link_skills(config_file, dry_run=False)

        captured = capsys.readouterr()
        assert "找不到" in captured.out or "不存在" in captured.out

    def test_links_skills_to_enabled_targets(self, tmp_path, capsys):
        """將 skills 複製到啟用的 targets"""
        # 建立 skill 來源
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        skill1 = skills_dir / "skill1"
        skill1.mkdir()
        (skill1 / "SKILL.md").write_text("skill1")

        skill2 = skills_dir / "skill2"
        skill2.mkdir()
        (skill2 / "SKILL.md").write_text("skill2")

        # 建立 config
        config_file = tmp_path / "test.toml"
        config_file.write_text(f"""
skills = ["skill1", "skill2"]

[sources]
paths = ["{skills_dir}"]

[targets.ide1]
path = "{tmp_path / "ide1" / "skills"}"
enabled = true

[targets.ide2]
path = "{tmp_path / "ide2" / "skills"}"
enabled = false
""")

        # 執行複製
        link_skills(config_file, dry_run=False)

        # 驗證：ide1 應該有複製的 skills
        ide1_skills = tmp_path / "ide1" / "skills"
        assert (ide1_skills / "skill1").is_dir()
        assert (ide1_skills / "skill2").is_dir()
        assert (ide1_skills / "skill1" / "SKILL.md").read_text() == "skill1"
        assert (ide1_skills / "skill2" / "SKILL.md").read_text() == "skill2"

        # 驗證：ide2 不應該有複製（未啟用）
        ide2_skills = tmp_path / "ide2" / "skills"
        assert not ide2_skills.exists()

    def test_creates_target_directory_if_missing(self, tmp_path):
        """自動建立不存在的目標目錄"""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        skill = skills_dir / "skill"
        skill.mkdir()
        (skill / "SKILL.md").write_text("content")

        config_file = tmp_path / "test.toml"
        config_file.write_text(f"""
skills = ["skill"]

[sources]
paths = ["{skills_dir}"]

[targets.ide]
path = "{tmp_path / "nonexistent" / "skills"}"
enabled = true
""")

        link_skills(config_file, dry_run=False)

        # 驗證目錄被建立
        assert (tmp_path / "nonexistent" / "skills").exists()
        assert (tmp_path / "nonexistent" / "skills" / "skill").is_dir()

    def test_dry_run_shows_preview(self, tmp_path, capsys):
        """Dry-run 模式顯示預覽"""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        skill = skills_dir / "skill"
        skill.mkdir()

        config_file = tmp_path / "test.toml"
        config_file.write_text(f"""
skills = ["skill"]

[sources]
paths = ["{skills_dir}"]

[targets.ide]
path = "{tmp_path / "ide" / "skills"}"
enabled = true
""")

        link_skills(config_file, dry_run=True)

        captured = capsys.readouterr()
        assert "Dry-run 模式" in captured.out
        assert "將建立目錄" in captured.out or "📁" in captured.out

        # 驗證沒有實際建立
        assert not (tmp_path / "ide").exists()

    def test_handles_missing_skills_gracefully(self, tmp_path, capsys):
        """優雅處理不存在的 skills"""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        config_file = tmp_path / "test.toml"
        config_file.write_text(f"""
skills = ["missing-skill"]

[sources]
paths = ["{skills_dir}"]

[targets.ide]
path = "{tmp_path / "ide" / "skills"}"
enabled = true
""")

        link_skills(config_file, dry_run=False)

        captured = capsys.readouterr()
        assert "找不到" in captured.out or "不存在" in captured.out
        assert "沒有可連結的 skills" in captured.out

        # 當沒有找到任何 skill 時，不會建立目標目錄
        assert not (tmp_path / "ide" / "skills").exists()

    def test_no_enabled_targets_shows_warning(self, tmp_path, capsys):
        """沒有啟用的 targets 時顯示警告"""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        skill = skills_dir / "skill"
        skill.mkdir()

        config_file = tmp_path / "test.toml"
        config_file.write_text(f"""
skills = ["skill"]

[sources]
paths = ["{skills_dir}"]

[targets.ide]
path = "{tmp_path / "ide" / "skills"}"
enabled = false
""")

        link_skills(config_file, dry_run=False)

        captured = capsys.readouterr()
        assert "沒有啟用的 targets" in captured.out

    def test_target_contains_only_configured_skills(self, tmp_path):
        """target 目錄下應該只包含 config 中定義的 skills"""
        # 建立 target 目錄並複製舊的 skill
        target_dir = tmp_path / "ide" / "skills"
        target_dir.mkdir(parents=True)
        old_target = target_dir / "old-skill"
        old_target.mkdir()
        (old_target / "SKILL.md").write_text("old skill")

        # 驗證舊的目錄存在
        assert old_target.is_dir()

        # 建立新的 skills
        new_skills_dir = tmp_path / "new_skills"
        new_skills_dir.mkdir()

        skill_1 = new_skills_dir / "skill-1"
        skill_1.mkdir()
        (skill_1 / "SKILL.md").write_text("skill 1")

        skill_2 = new_skills_dir / "skill-2"
        skill_2.mkdir()
        (skill_2 / "SKILL.md").write_text("skill 2")

        # 建立 config，只包含新的 skills
        config_file = tmp_path / "test.toml"
        config_file.write_text(f"""
skills = ["skill-1", "skill-2"]

[sources]
paths = ["{new_skills_dir}"]

[targets.ide]
path = "{target_dir}"
enabled = true
""")

        # 執行複製
        link_skills(config_file, dry_run=False)

        # 驗證：target 目錄下應該只有 config 中定義的 skills
        skills_in_target = [p.name for p in target_dir.iterdir()]
        assert set(skills_in_target) == {"skill-1", "skill-2"}

        # 驗證：舊的 skill 應該被移除
        assert not (target_dir / "old-skill").exists()

        # 驗證：新的 skills 應該被正確複製
        assert (target_dir / "skill-1").is_dir()
        assert (target_dir / "skill-2").is_dir()
        assert (target_dir / "skill-1" / "SKILL.md").read_text() == "skill 1"
        assert (target_dir / "skill-2" / "SKILL.md").read_text() == "skill 2"

    def test_dry_run_shows_skills_to_remove(self, tmp_path, capsys):
        """dry_run 模式下應該顯示將要移除的 skills"""
        # 建立 target 目錄並複製舊的 skill
        target_dir = tmp_path / "ide" / "skills"
        target_dir.mkdir(parents=True)
        old_target = target_dir / "old-skill"
        old_target.mkdir()
        (old_target / "SKILL.md").write_text("old skill")

        # 建立新的 skills
        new_skills_dir = tmp_path / "new_skills"
        new_skills_dir.mkdir()

        skill_1 = new_skills_dir / "skill-1"
        skill_1.mkdir()
        (skill_1 / "SKILL.md").write_text("skill 1")

        # 建立 config，只包含新的 skill
        config_file = tmp_path / "test.toml"
        config_file.write_text(f"""
skills = ["skill-1"]

[sources]
paths = ["{new_skills_dir}"]

[targets.ide]
path = "{target_dir}"
enabled = true
""")

        # 執行 dry_run
        link_skills(config_file, dry_run=True)

        # 驗證：輸出中應該包含將要移除的訊息
        captured = capsys.readouterr()
        assert "old-skill" in captured.out
        assert "將移除" in captured.out or "🗑️" in captured.out

        # 驗證：舊的 skill 應該還存在（因為是 dry_run）
        assert old_target.is_dir()

        # 驗證：新的 skill 不應該被建立（因為是 dry_run）
        assert not (target_dir / "skill-1").exists()

    def test_updates_existing_skills(self, tmp_path, capsys):
        """當 skills 已經存在時，應該更新它們"""
        # 建立 skill 來源
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        skill = skills_dir / "test-skill"
        skill.mkdir()
        (skill / "SKILL.md").write_text("new content")

        # 建立 target 目錄並預先建立舊的目錄
        target_dir = tmp_path / "ide" / "skills"
        target_dir.mkdir(parents=True)
        old_skill = target_dir / "test-skill"
        old_skill.mkdir()
        (old_skill / "SKILL.md").write_text("old content")

        # 建立 config
        config_file = tmp_path / "test.toml"
        config_file.write_text(f"""
skills = ["test-skill"]

[sources]
paths = ["{skills_dir}"]

[targets.ide]
path = "{target_dir}"
enabled = true
""")

        # 執行複製（非 dry-run）
        link_skills(config_file, dry_run=False)

        # 驗證：目錄應該被更新
        captured = capsys.readouterr()
        assert "更新" in captured.out or "🔄" in captured.out

        # 驗證：內容應該是新的
        assert (old_skill / "SKILL.md").read_text() == "new content"

        # 應該包含統計資訊
        assert "✨" in captured.out
        assert "完成" in captured.out

    def test_dry_run_shows_correct_statistics_for_new_skills(
        self, tmp_path, capsys
    ):
        """dry-run 模式下，統計數字應該正確反映將要建立的 skills 數量"""
        # 建立 skill 來源
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        skill1 = skills_dir / "skill-1"
        skill1.mkdir()
        (skill1 / "SKILL.md").write_text("skill 1")

        skill2 = skills_dir / "skill-2"
        skill2.mkdir()
        (skill2 / "SKILL.md").write_text("skill 2")

        # 建立 target 目錄（空的，沒有預先建立任何連結）
        target_dir = tmp_path / "ide" / "skills"
        target_dir.mkdir(parents=True)

        # 建立 config
        config_file = tmp_path / "test.toml"
        config_file.write_text(f"""
skills = ["skill-1", "skill-2"]

[sources]
paths = ["{skills_dir}"]

[targets.ide]
path = "{target_dir}"
enabled = true
""")

        # 執行 dry-run
        link_skills(config_file, dry_run=True)

        # 驗證：統計應該顯示「更新/複製 2」（因為有 2 個新的 skills）
        captured = capsys.readouterr()
        assert "更新/複製 2" in captured.out
        assert "共 2/2" in captured.out


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


class TestCoverageGaps:
    """測試未覆蓋的程式碼路徑"""

    def test_dry_run_shows_overwrite_message(self, tmp_path, capsys):
        """dry-run 模式下覆蓋已存在 target 時的訊息（line 87）"""
        source = tmp_path / "source_skill"
        source.mkdir()
        (source / "SKILL.md").write_text("new")

        target_dir = tmp_path / "target"
        target_dir.mkdir()
        target = target_dir / "existing_dir"
        target.mkdir()
        (target / "SKILL.md").write_text("old")

        result = copy_skill(source, target, dry_run=True)

        assert result is True
        captured = capsys.readouterr()
        assert "將覆蓋" in captured.out or "🔄" in captured.out

    def test_new_format_without_sources_paths_shows_warning(
        self, tmp_path, capsys
    ):
        """新格式 config 沒有 sources.paths 時顯示警告"""
        config_file = tmp_path / "test.toml"
        config_file.write_text("""
skills = ["skill1", "skill2"]

[sources]
# paths 是空的

[targets.ide]
path = "./ide/skills"
enabled = true
""")

        link_skills(config_file, dry_run=False)

        captured = capsys.readouterr()
        assert "sources.paths" in captured.out

    def test_empty_or_invalid_skills_format_shows_warning(
        self, tmp_path, capsys
    ):
        """無效的 skills 格式顯示警告"""
        config_file = tmp_path / "test.toml"
        config_file.write_text("""
skills = []

[targets.ide]
path = "./ide/skills"
enabled = true
""")

        link_skills(config_file, dry_run=False)

        captured = capsys.readouterr()
        # 空的 skills 列表會觸發警告
        assert "skills" in captured.out.lower() or "沒有" in captured.out

    def test_config_without_targets_shows_warning(self, tmp_path, capsys):
        """config 中沒有 targets 時顯示警告（lines 175-176）"""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        skill = skills_dir / "skill"
        skill.mkdir()

        config_file = tmp_path / "test.toml"
        config_file.write_text(f"""
skills = ["skill"]

[sources]
paths = ["{skills_dir}"]
""")

        link_skills(config_file, dry_run=False)

        captured = capsys.readouterr()
        assert "targets" in captured.out.lower()

    def test_removes_directory_not_in_config(self, tmp_path, capsys):
        """移除不在 config 中的目錄（非 symlink）（lines 222-224）"""
        # 建立 target 目錄，裡面有一個真實目錄（非 symlink）
        target_dir = tmp_path / "ide" / "skills"
        target_dir.mkdir(parents=True)
        old_dir = target_dir / "old-dir-skill"
        old_dir.mkdir()
        (old_dir / "file.txt").write_text("content")

        # 建立新的 skill
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        new_skill = skills_dir / "new-skill"
        new_skill.mkdir()

        config_file = tmp_path / "test.toml"
        config_file.write_text(f"""
skills = ["new-skill"]

[sources]
paths = ["{skills_dir}"]

[targets.ide]
path = "{target_dir}"
enabled = true
""")

        link_skills(config_file, dry_run=False)

        captured = capsys.readouterr()
        # 舊目錄應該被移除
        assert not old_dir.exists()
        assert "old-dir-skill" in captured.out
        assert "已移除" in captured.out or "🗑️" in captured.out

    def test_updates_existing_directory(self, tmp_path, capsys):
        """更新已存在的目錄（lines 251-256）"""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        new_source = skills_dir / "skill"
        new_source.mkdir()
        (new_source / "new.md").write_text("new")

        target_dir = tmp_path / "ide" / "skills"
        target_dir.mkdir(parents=True)
        # 建立舊的目錄
        old_target = target_dir / "skill"
        old_target.mkdir()
        (old_target / "old.md").write_text("old")

        config_file = tmp_path / "test.toml"
        config_file.write_text(f"""
skills = ["skill"]

[sources]
paths = ["{skills_dir}"]

[targets.ide]
path = "{target_dir}"
enabled = true
""")

        link_skills(config_file, dry_run=False)

        captured = capsys.readouterr()
        # 應該更新目錄
        assert (target_dir / "skill").is_dir()
        assert (target_dir / "skill" / "new.md").read_text() == "new"
        assert not (target_dir / "skill" / "old.md").exists()
        assert "更新" in captured.out or "🔄" in captured.out

    def test_overwrites_existing_file_not_directory(self, tmp_path, capsys):
        """覆蓋已存在的檔案（非目錄）（lines 262-266）"""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        source = skills_dir / "skill"
        source.mkdir()
        (source / "SKILL.md").write_text("content")

        target_dir = tmp_path / "ide" / "skills"
        target_dir.mkdir(parents=True)
        # 建立一個普通檔案（非目錄）
        fake_skill = target_dir / "skill"
        fake_skill.write_text("this is a file")

        config_file = tmp_path / "test.toml"
        config_file.write_text(f"""
skills = ["skill"]

[sources]
paths = ["{skills_dir}"]

[targets.ide]
path = "{target_dir}"
enabled = true
""")

        link_skills(config_file, dry_run=False)

        # 應該覆蓋檔案並建立目錄
        assert (target_dir / "skill").is_dir()
        assert (target_dir / "skill" / "SKILL.md").read_text() == "content"

    def test_dry_run_updates_directory_shows_message(self, tmp_path, capsys):
        """dry-run 模式下更新目錄的訊息（line 251-252）"""
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        new_source = skills_dir / "skill"
        new_source.mkdir()
        (new_source / "new.md").write_text("new")

        target_dir = tmp_path / "ide" / "skills"
        target_dir.mkdir(parents=True)
        old_target = target_dir / "skill"
        old_target.mkdir()
        (old_target / "old.md").write_text("old")

        config_file = tmp_path / "test.toml"
        config_file.write_text(f"""
skills = ["skill"]

[sources]
paths = ["{skills_dir}"]

[targets.ide]
path = "{target_dir}"
enabled = true
""")

        link_skills(config_file, dry_run=True)

        captured = capsys.readouterr()
        # dry-run 模式下應該顯示將要更新的訊息
        assert "將更新" in captured.out or "🔄" in captured.out
        # 目錄應該保持舊內容
        assert (old_target / "old.md").exists()
        assert not (old_target / "new.md").exists()

    def test_removes_symlink_not_in_config(self, tmp_path, capsys):
        """移除不在 config 中的 symlink（line 219-221）"""
        # 建立一個真實的 skill 目錄作為 symlink 來源
        real_skill = tmp_path / "real-skill"
        real_skill.mkdir()
        (real_skill / "file.txt").write_text("content")

        # 建立 target 目錄，裡面有一個 symlink
        target_dir = tmp_path / "ide" / "skills"
        target_dir.mkdir(parents=True)
        old_symlink = target_dir / "old-symlink-skill"
        old_symlink.symlink_to(real_skill)

        # 驗證 symlink 存在
        assert old_symlink.is_symlink()
        assert old_symlink.exists()

        # 建立新的 skill
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        new_skill = skills_dir / "new-skill"
        new_skill.mkdir()
        (new_skill / "SKILL.md").write_text("new skill")

        config_file = tmp_path / "test.toml"
        config_file.write_text(f"""
skills = ["new-skill"]

[sources]
paths = ["{skills_dir}"]

[targets.ide]
path = "{target_dir}"
enabled = true
""")

        link_skills(config_file, dry_run=False)

        captured = capsys.readouterr()
        # symlink 應該被移除
        assert not old_symlink.exists()
        assert "old-symlink-skill" in captured.out
        assert "symlink" in captured.out.lower()
        assert "已移除" in captured.out or "🗑️" in captured.out

        # 新的 skill 應該被複製
        assert (target_dir / "new-skill").is_dir()
        assert (target_dir / "new-skill" / "SKILL.md").read_text() == "new skill"

    def test_updates_existing_symlink(self, tmp_path, capsys):
        """更新已存在的 symlink（line 248-249）"""
        # 建立一個真實的 skill 目錄作為 symlink 來源
        old_real_skill = tmp_path / "old-real-skill"
        old_real_skill.mkdir()
        (old_real_skill / "old.md").write_text("old")

        # 建立 target 目錄，裡面有一個指向舊 skill 的 symlink
        target_dir = tmp_path / "ide" / "skills"
        target_dir.mkdir(parents=True)
        skill_link = target_dir / "skill"
        skill_link.symlink_to(old_real_skill)

        # 驗證 symlink 存在
        assert skill_link.is_symlink()
        assert skill_link.exists()

        # 建立新的 skill 來源
        skills_dir = tmp_path / "skills"
        skills_dir.mkdir()

        new_source = skills_dir / "skill"
        new_source.mkdir()
        (new_source / "new.md").write_text("new")

        config_file = tmp_path / "test.toml"
        config_file.write_text(f"""
skills = ["skill"]

[sources]
paths = ["{skills_dir}"]

[targets.ide]
path = "{target_dir}"
enabled = true
""")

        link_skills(config_file, dry_run=False)

        captured = capsys.readouterr()
        # symlink 應該被移除並替換為真實目錄
        assert not skill_link.is_symlink()
        assert skill_link.is_dir()
        assert (skill_link / "new.md").read_text() == "new"
        assert not (skill_link / "old.md").exists()
        assert "更新" in captured.out or "🔄" in captured.out
