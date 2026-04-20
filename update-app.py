import os
path = r'C:\Users\Abhishek\Downloads\lifescan\smartflow\src\App.jsx'
with open(path, 'r', encoding='utf-8') as f: content = f.read()

import_line = "import FanScore from './components/dashboard/FanScore';\nimport LiveTrivia from './components/dashboard/LiveTrivia';"
content = content.replace("import FanScore from './components/dashboard/FanScore';", import_line)

render_line = "<FanScore orders={orderCount} />\n        <LiveTrivia onEarnPoints={() => setOrderCount(c => c + 1)} />"
content = content.replace("<FanScore orders={orderCount} />", render_line)

with open(path, 'w', encoding='utf-8') as f: f.write(content)
