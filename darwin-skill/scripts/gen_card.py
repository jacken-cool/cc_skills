"""Generate result card HTML with actual evaluation data."""
import re

template_path = "C:/Users/EDY/.claude/skills/darwin-skill/templates/result-card.html"
output_path = "C:/Users/EDY/.claude/skills/darwin-skill/card_output.html"

with open(template_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Add CSS for unchanged dim cells and flat arrow
html = html.replace(
    '.dim-cell {\n    background: #F0EBE3;',
    '.dim-cell {\n    background: #F0EBE3;\n    opacity: 0.85;'
)
html = html.replace(
    '.dim-cell.hot {',
    '.dim-cell.nochange { opacity: 0.55; }\n  .dim-cell.hot {'
)
html = html.replace(
    '.dim-arrow.up-small {',
    '.dim-arrow.flat { background: #E8E4DE; color: #AAA; }\n  .dim-arrow.up-small {'
)

# Brand bar date
html = html.replace('data-field="date">2026.04.14</div>', 'data-field="date">2026.05.12</div>')

# Hero section
html = html.replace(
    'data-field="skill-name">审校降AI味</span>',
    'data-field="skill-name">测试一条龙交付</span>'
)
html = html.replace(
    'data-field="score-before">72</strong>',
    'data-field="score-before">63</strong>'
)
html = html.replace(
    'data-field="score-after">87',
    'data-field="score-after">75'
)
html = html.replace(
    'data-field="skill-id">huashu-proofreading</span>',
    'data-field="skill-id">buddyskill-auxre-to-test-suite</span>'
)
html = html.replace(
    'data-field="score-delta">+15',
    'data-field="score-delta">+12'
)
html = html.replace(
    '从 <strong data-field="score-before">63</strong> 分进化到 <strong>87</strong> 分',
    '从 <strong data-field="score-before">63</strong> 分进化到 <strong>75</strong> 分'
)

# Ring progress: full circle=534, for 75/100 → offset=534*0.25=133.5
html = html.replace('stroke-dashoffset: 69;', 'stroke-dashoffset: 133.5;')

# Breakthrough cards
html = html.replace(
    'data-field="top1-name">指令精度</div>',
    'data-field="top1-name">资源整合度</div>'
)
html = html.replace(
    'data-field="top1-from">5</span>',
    'data-field="top1-from">3</span>'
)
html = html.replace(
    'data-field="top1-to">9</span>',
    'data-field="top1-to">7</span>'
)
html = html.replace(
    'data-field="top1-pct">+80%</div>',
    'data-field="top1-pct">+133%</div>'
)
html = html.replace(
    'data-field="top1-story">从模糊指令到精确可执行，指令精度翻了将近一倍</div>',
    'data-field="top1-story">清理10个死引用，所有文件路径可验证</div>'
)

html = html.replace(
    'data-field="top2-name">工作流清晰度</div>',
    'data-field="top2-name">整体架构</div>'
)
html = html.replace(
    'data-field="top2-from">5</span>',
    'data-field="top2-from">5</span>'
)
html = html.replace(
    'data-field="top2-to">8</span>',
    'data-field="top2-to">8</span>'
)
html = html.replace(
    'data-field="top2-pct">+60%</div>',
    'data-field="top2-pct">+60%</div>'
)
html = html.replace(
    'data-field="top2-story">线性可执行步骤，每步都有明确检查点</div>',
    'data-field="top2-story">去除tools矩阵+B2精简30行→10行</div>'
)

# Dimensions grid - replace all 8 cells
dims = [
    ("元数据", 4, 7, "+3", "up-big", "hot"),
    ("工作流", 7, 8, "+1", "up-small", "warm"),
    ("边界覆盖", 8, 8, "--", "flat", "nochange"),
    ("检查点", 8, 8, "--", "flat", "nochange"),
    ("指令精度", 6, 7, "+1", "up-small", "warm"),
    ("资源整合", 3, 7, "+4", "up-big", "hot"),
    ("整体架构", 5, 8, "+3", "up-big", "hot"),
    ("实测表现", 7, 7, "--", "flat", "nochange"),
]

dim_cells = []
for name, old, new, delta, arrow_cls, cell_cls in dims:
    dim_cells.append(f'''      <div class="dim-cell {cell_cls}">
        <div class="dim-name">{name}</div>
        <div class="dim-score-row">
          <span class="dim-old-score">{old}</span>
          <span class="dim-score">{new}</span>
        </div>
        <span class="dim-arrow {arrow_cls}">{delta}</span>
      </div>''')

new_grid_marker_start = '      <div class="dim-cell warm">\n        <div class="dim-name">元数据</div>'
new_grid_marker_end = '      </div>\n    </div>\n  </div>'

# Find and replace the entire dims grid
start_idx = html.find(new_grid_marker_start)
end_idx = html.find(new_grid_marker_end, start_idx) + len(new_grid_marker_end)
if start_idx >= 0 and end_idx > start_idx:
    html = html[:start_idx] + '\n'.join(dim_cells) + '\n    </div>\n  </div>' + html[end_idx:]

# Summary items
html = html.replace(
    'data-field="improve-1">补充异常处理fallback路径，边界覆盖从4飙升到7</div>',
    'data-field="improve-1">清理tools/目录等10个死链接，资源整合度 3\xe2\x86\x927（+133%）</div>'
)
html = html.replace(
    'data-field="improve-2">工作流重组为线性可执行步骤，每步可验证</div>',
    'data-field="improve-2">补充11个触发关键词+更新能力描述，Frontmatter从裸空到完整</div>'
)
html = html.replace(
    'data-field="improve-3">测试prompt覆盖率从60%提升到95%，实测表现大幅进化</div>',
    'data-field="improve-3">精简B2会话参数段（30→10行）+B3直接路径映射，架构清晰度大幅提升</div>'
)

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Card saved: {output_path}")
