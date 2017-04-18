Add-Type -Assembly "system.io.compression.filesystem"
$source = "Z:\Avelino\Videos\GeckoVideo\Curro"
$destination = "D:\Curro.zip"
$level = [System.IO.Compression.CompressionLevel]::Optimal
$include = $true
[io.compression.zipfile]::CreateFromDirectory($source, $destination, $level, $Include)