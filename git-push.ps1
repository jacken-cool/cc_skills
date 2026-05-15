# Git 一键推送脚本
# 双击 git-push.bat 运行，或：powershell -ExecutionPolicy Bypass -File git-push.ps1

$remote = "skills"
$branch = "master"
$repoUrl = "github.com/jacken-cool/cc_skills"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$hasError = $false

Write-Host "===== Git 一键推送 =====" -ForegroundColor Cyan
Write-Host "远程: $remote ($repoUrl)"
Write-Host "分支: $branch"
Write-Host ""

# 1. git add
Write-Host "[1/3] 添加所有变更..." -ForegroundColor Yellow
git add -A
if ($LASTEXITCODE -ne 0) {
    Write-Host "[失败] git add 出错" -ForegroundColor Red
    $hasError = $true
}

# 2. git commit
if (-not $hasError) {
    Write-Host "[2/3] 提交..." -ForegroundColor Yellow
    git commit -m "update $timestamp"
    if ($LASTEXITCODE -eq 1) {
        Write-Host "[提示] 没有变更需要提交" -ForegroundColor Yellow
        $hasError = $true
    } elseif ($LASTEXITCODE -ne 0) {
        Write-Host "[失败] git commit 出错" -ForegroundColor Red
        $hasError = $true
    }
}

# 3. git push
if (-not $hasError) {
    Write-Host "[3/3] 推送到远程..." -ForegroundColor Yellow
    git push $remote $branch
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[失败] git push 出错" -ForegroundColor Red
        $hasError = $true
    }
}

Write-Host ""
if ($hasError) {
    Write-Host "===== 执行完毕（请检查上方错误信息）=====" -ForegroundColor Red
} else {
    Write-Host "===== 推送完成 =====" -ForegroundColor Green
}
pause
