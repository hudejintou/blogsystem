@echo off
cd /d %~dp0

for /f "tokens=*" %%i in ('git status --porcelain') do set has_change=1
if not defined has_change (
    echo 没有变更，无需存档。
    exit /b 0
)

echo === 变更文件 ===
git status --short

set /p msg="输入提交信息 (回车默认存档时间): "
if "%msg%"=="" (
    set msg=存档 %date:~0,10% %time:~0,5%
)

git add -A
git commit -m "%msg%"
git push
echo === 存档完成 ===
