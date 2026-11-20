#!/bin/zsh
# usage: check.sh <width> [page]  → 本物の<width>px幅（iframe）で横スクロール/見出しはみ出しを判定し、全長スクショを撮る
cd ${0:A:h}/..
W=$1; P=${2:-index.html}; CH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
mkdir -p _tools/shots
sed 's#</body>#<script>window.addEventListener("load",function(){setTimeout(function(){var o=[];document.querySelectorAll("h1,h2").forEach(function(e){if(e.scrollWidth>e.clientWidth+1)o.push(e.textContent)});parent.postMessage("SW="+document.documentElement.scrollWidth+" VW="+innerWidth+" H="+document.documentElement.scrollHeight+" OVER="+JSON.stringify(o),"*")},1500)})</script></body>#' $P > _check.html
run(){ "$CH" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 "$@" 2>/dev/null }
wrap(){ echo "<html><body style=margin:0><iframe src=_check.html width=$W height=$1 style=border:0;display:block></iframe><pre id=r></pre><script>addEventListener('message',function(e){document.getElementById('r').textContent=e.data})</script></body></html>" > _wrap.html }
wrap 900; R=$(run --window-size=600,900 --virtual-time-budget=8000 --dump-dom "file://$PWD/_wrap.html" | grep -o 'SW=[^<]*'); echo "$R"
H=$(echo $R | grep -o 'H=[0-9]*' | cut -d= -f2)
wrap $H; run --window-size=600,$H --virtual-time-budget=8000 --screenshot=$PWD/_tools/shots/$W.png "file://$PWD/_wrap.html"
python3 -c "import sys;from PIL import Image;i=Image.open(sys.argv[1]);i.crop((0,0,int(sys.argv[2]),i.height)).save(sys.argv[1])" _tools/shots/$W.png $W; rm _check.html _wrap.html; echo shot _tools/shots/$W.png
