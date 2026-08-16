$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location (Join-Path $root "haskell")
runghc Main.hs
