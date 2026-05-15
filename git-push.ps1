# Git 一键推送脚本（双远程）
# 双击 git-push.bat 运行，或：powershell -ExecutionPolicy Bypass -File git-push.ps1

$remotes = @("skills", "gitee")
$branch = "master"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

Write-Host "===== Git 一键推送（双远程）=====" -ForegroundColor Cyan
Write-Host "目标: skills (github.com/jacken-cool/cc_skills)" -ForegroundColor Gray
Write-Host "      gitee (gitee.com/sjk314/cc_skills)" -ForegroundColor Gray
Write-Host "分支: $branch"
Write-Host ""

# 1. git add
Write-Host "[1/3] 添加所有变更..." -ForegroundColor Yellow
git add -A
if ($LASTEXITCODE -ne 0) {
    Write-Host "[失败] git add 出错" -ForegroundColor Red
    pause
    exit 1
}

# 2. git commit
Write-Host "[2/3] 提交..." -ForegroundColor Yellow
git commit -m "update $timestamp"
if ($LASTEXITCODE -eq 1) {
    Write-Host "[提示] 没有变更需要提交" -ForegroundColor Yellow
    pause
    exit 0
} elseif ($LASTEXITCODE -ne 0) {
    Write-Host "[失败] git commit 出错" -ForegroundColor Red
    pause
    exit 1
}

# 3. git push (both remotes)
Write-Host "[3/3] 推送到远程..." -ForegroundColor Yellow
$pushOk = $true
foreach ($remote in $remotes) {
    Write-Host "  -> $remote ..." -NoNewline
    git push $remote $branch
    if ($LASTEXITCODE -eq 0) {
        Write-Host " OK" -ForegroundColor Green
    } else {
        Write-Host " 失败" -ForegroundColor Red
        $pushOk = $false
    }
}

Write-Host ""
if ($pushOk) {
    Write-Host "===== 推送完成 =====" -ForegroundColor Green
} else {
    Write-Host "===== 部分推送失败（请检查上方错误信息）=====" -ForegroundColor Red
}
pause
