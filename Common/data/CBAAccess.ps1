$CCPHost = 'cyberarkccp.homecredit.vn'
$appID = "umc"
$safe = "IT_Service_Desk _Safe"
$accountObject = "umc_admin"
$certThumbprint = "6b14c3c96dc592c364f5a3ef642db09195550cb6"
# certThumbprint is the thumbprint of the certificate that will use for authentication with Cyberark
#If calling the cert from Current User cert store:
$certPath = "Cert:\CurrentUser\My\" + $certThumbprint
#If calling the cert from Local Machine cert store:
#$certPath = "Cert:\CurrentUser\My\" + $certThumbprint
$myCert = Get-ChildItem -Path $certPath
#Write-Host = $myCert
$uriString = "https://" + $CCPHost + "/AIMWebService/api/Accounts?AppID=" + $appID + "&Query=Safe=" + $safe + ";Object=" + $accountObject
$content = Invoke-RestMethod -Method Get -Uri $uriString -ContentType application/json -Certificate $myCert | ConvertTo-Json
$cred = ($content | ConvertFrom-Json).Content

Write-Host $cred