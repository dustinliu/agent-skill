.PHONY: test lint format-check ci clean help

# 預設目標：顯示幫助
help:
	@echo "可用的指令："
	@echo "  make test         - 執行測試並生成覆蓋率報告（需達 80%）"
	@echo "  make lint         - 執行靜態分析（ruff check）"
	@echo "  make format-check - 檢查程式碼格式"
	@echo "  make ci           - 執行完整的 CI 流程（test + lint + format-check）"
	@echo "  make clean        - 清理生成的檔案"

# 執行測試（包含覆蓋率檢查）
test:
	uv run pytest
	uv run coverage report

# 靜態分析
lint:
	uv run ruff check .

# 檢查程式碼格式
format-check:
	uv run ruff format --check .

# 完整 CI 流程：測試 + 靜態分析 + 格式檢查
ci: test lint format-check
	@echo "✅ 所有檢查都通過了！"

# 清理生成的檔案
clean:
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
