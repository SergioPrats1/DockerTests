

$ScriptBlock = {
    
    param($TargetFile)

    $mutex = new-object System.Threading.Mutex $false,'FileExclusion'

    $response = Invoke-WebRequest -URI http://172.17.41.90:31234/
    [string[]] $lines = $response.Content.Split([Environment]::NewLine)
    
    $mutex.WaitOne() > $null
    $lines[2] >> $TargetFile

    $mutex.ReleaseMutex()
    
}

$mutex = new-object System.Threading.Mutex $false,'FileExclusion'

$TargetFile = $PSScriptRoot + "\RespondingHostName.txt"

"Host names for each execution:" | Out-File -FilePath .\RespondingHostName.txt

for ($i=1;$i -le 200;$i++) {
    
    Start-Job $ScriptBlock -ArgumentList $TargetFile
}


Get-Job

# Wait for it all to complete
While (Get-Job -State "Running")
{
  echo "awaiting background jobs to end"
  Start-Sleep 3
}


#Get-Job | Receive-Job

echo "Script completed"
