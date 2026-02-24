const pptxgen = require("pptxgenjs");

// ========== 统一配色 ==========
const C = {
  BLUE: '1565C0', LBLUE: '42A5F5', XLBLUE: '90CAF9', XXLBLUE: 'BBDEFB', BGBLUE: 'E3F2FD',
  GREEN: '4CAF50', BGGREEN: 'E8F5E9', DKGREEN: '2E7D32',
  PURPLE: '7B1FA2', BGPURPLE: 'F3E5F5',
  RED: 'E53935', DKRED: 'C62828', BGRED: 'FFEBEE',
  GOLD: 'F9A825', DKGOLD: 'E65100', BGGOLD: 'FFF8E1',
  TEXT: '212121', GRAY: '757575', LGRAY: 'E0E0E0', XLGRAY: 'F5F5F5',
  WHITE: 'FFFFFF',
};

// 字号基准（印刷170mm宽，最小字号16pt≈5.6mm）
const F = {
  TITLE: 24, SUBTITLE: 14,
  BOX_MAIN: 18, BOX_SUB: 12,
  LABEL: 16, SMALL: 13,
  HEADER: 20, CELL: 16,
  LEGEND: 13, NOTE: 12,
};

// ========== Slide 1: 图1-4 八原理层次图 ==========
function slide_01_04(pres) {
  let s = pres.addSlide();
  s.background = { color: C.WHITE };

  // Title
  s.addText([
    { text: '图 1-4　CHS八原理层次关系图', options: { fontSize: F.TITLE, bold: true, color: C.TEXT, breakLine: true } },
    { text: 'Fig. 1-4 Hierarchical Structure of CHS Eight Principles', options: { fontSize: F.SUBTITLE, color: C.GRAY } },
  ], { x: 0.3, y: 0.15, w: 9.4, h: 0.8, align: 'center', valign: 'top' });

  // 五层定义
  const layers = [
    { y: 1.05, h: 1.05, label: '演进层', labelEn: 'Evolution', bg: C.BGGOLD, border: C.GOLD,
      boxes: [{ x: 3.2, w: 3.6, name: 'P8 自主演进', nameEn: 'Autonomous Evolution', fg: C.DKGOLD, border: C.GOLD }]
    },
    { y: 2.25, h: 1.15, label: '智能层', labelEn: 'Intelligence', bg: C.BGPURPLE, border: C.PURPLE,
      boxes: [
        { x: 2.2, w: 2.7, name: 'P6 认知增强', nameEn: 'Cognitive AI', fg: C.PURPLE, border: C.PURPLE },
        { x: 5.2, w: 2.7, name: 'P7 人机共融', nameEn: 'Human-Machine', fg: C.PURPLE, border: C.PURPLE },
      ]
    },
    { y: 3.55, h: 1.05, label: '验证层', labelEn: 'Verification', bg: C.BGGREEN, border: C.GREEN,
      boxes: [{ x: 2.8, w: 4.4, name: 'P5 在环验证', nameEn: 'xIL (MIL/SIL/HIL)', fg: C.DKGREEN, border: C.GREEN }]
    },
    { y: 4.75, h: 1.15, label: '架构层', labelEn: 'Architecture', bg: C.BGBLUE, border: C.BLUE,
      boxes: [
        { x: 2.2, w: 2.7, name: 'P3 分层分布式', nameEn: 'HDC', fg: C.BLUE, border: C.BLUE },
        { x: 5.2, w: 2.7, name: 'P4 安全包络', nameEn: 'Safety Envelope', fg: C.DKRED, border: C.RED, boxBg: C.BGRED },
      ]
    },
    { y: 6.05, h: 1.15, label: '基础层', labelEn: 'Foundation', bg: C.BGBLUE, border: C.BLUE,
      boxes: [
        { x: 2.2, w: 2.7, name: 'P1 传递函数化', nameEn: 'Transfer Function', fg: C.BLUE, border: C.BLUE },
        { x: 5.2, w: 2.7, name: 'P2 可控可观性', nameEn: 'Controllability', fg: C.BLUE, border: C.BLUE },
      ]
    },
  ];

  layers.forEach(layer => {
    // Layer background
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x: 0.5, y: layer.y, w: 8.0, h: layer.h,
      fill: { color: layer.bg }, line: { color: layer.border, width: 2 }, rectRadius: 0.08,
    });
    // Layer label
    s.addText([
      { text: layer.label, options: { fontSize: F.BOX_MAIN, bold: true, color: layer.border, breakLine: true } },
      { text: layer.labelEn, options: { fontSize: F.SMALL, color: layer.border } },
    ], { x: 0.65, y: layer.y + 0.1, w: 1.3, h: layer.h - 0.2, valign: 'middle', margin: 0 });

    // Boxes
    layer.boxes.forEach(box => {
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
        x: box.x, y: layer.y + 0.12, w: box.w, h: layer.h - 0.24,
        fill: { color: box.boxBg || C.WHITE }, line: { color: box.border, width: 2 }, rectRadius: 0.06,
      });
      s.addText([
        { text: box.name, options: { fontSize: F.BOX_MAIN, bold: true, color: box.fg, breakLine: true } },
        { text: box.nameEn, options: { fontSize: F.BOX_SUB, color: box.fg } },
      ], { x: box.x, y: layer.y + 0.12, w: box.w, h: layer.h - 0.24, align: 'center', valign: 'middle', margin: 0 });
    });
  });

  // 层间向上箭头
  const arrowYs = [5.92, 4.62, 3.42, 2.12]; // bottom of gap positions
  arrowYs.forEach(ay => {
    s.addShape(pres.shapes.LINE, {
      x: 5.0, y: ay, w: 0, h: -0.12,
      line: { color: C.GRAY, width: 2, endArrowType: 'triangle' },
    });
  });

  // P4→P8 红色约束弧线 (用文字标注代替，PPT中用户可自行画弧)
  s.addShape(pres.shapes.LINE, {
    x: 8.7, y: 1.55, w: 0, h: 4.2,
    line: { color: C.RED, width: 3, dashType: 'lgDash' },
  });
  // Arrow head at top
  s.addShape(pres.shapes.LINE, {
    x: 8.5, y: 1.55, w: 0.2, h: 0.2,
    line: { color: C.RED, width: 3 },
  });
  s.addShape(pres.shapes.LINE, {
    x: 8.7, y: 1.55, w: 0.2, h: 0.2,
    line: { color: C.RED, width: 3 },
  });
  s.addText([
    { text: '安全约束', options: { fontSize: F.LABEL, bold: true, color: C.DKRED, breakLine: true } },
    { text: 'Safety', options: { fontSize: F.SMALL, color: C.RED, breakLine: true } },
    { text: 'Constraint', options: { fontSize: F.SMALL, color: C.RED } },
  ], { x: 8.4, y: 3.2, w: 1.3, h: 1.0, align: 'center', valign: 'middle', margin: 0 });

  // Legend
  s.addShape(pres.shapes.LINE, { x: 0.5, y: 7.35, w: 0.5, h: 0, line: { color: C.GRAY, width: 2 } });
  s.addText('层间依赖', { x: 1.1, y: 7.25, w: 1.2, h: 0.25, fontSize: F.LEGEND, color: C.GRAY, margin: 0 });
  s.addShape(pres.shapes.LINE, { x: 2.5, y: 7.35, w: 0.8, h: 0, line: { color: C.RED, width: 3, dashType: 'lgDash' } });
  s.addText('P4安全约束 → P8演进上界', { x: 3.4, y: 7.25, w: 3.5, h: 0.25, fontSize: F.LEGEND, bold: true, color: C.RED, margin: 0 });
}

// ========== Slide 2: 图2-2 金字塔 ==========
function slide_02_02(pres) {
  let s = pres.addSlide();
  s.background = { color: C.WHITE };

  s.addText([
    { text: '图 2-2　可控模型族的三层体系', options: { fontSize: F.TITLE, bold: true, color: C.TEXT, breakLine: true } },
    { text: 'Fig. 2-2 Three-Layer Controllable Model Family', options: { fontSize: F.SUBTITLE, color: C.GRAY } },
  ], { x: 0.3, y: 0.15, w: 9.4, h: 0.8, align: 'center', valign: 'top' });

  // 用三个递减宽度的矩形模拟金字塔（PPT中可手动调成梯形）
  // PBM bottom
  s.addShape(pres.shapes.TRAPEZOID, {
    x: 0.8, y: 4.6, w: 8.4, h: 1.8,
    fill: { color: C.BLUE }, line: { color: C.WHITE, width: 2 },
    rotate: 180,
  });
  s.addText([
    { text: 'PBM 高保真物理模型', options: { fontSize: 20, bold: true, color: C.WHITE, breakLine: true } },
    { text: 'Physics-Based Model', options: { fontSize: F.BOX_SUB, color: C.WHITE, breakLine: true } },
    { text: 'Saint-Venant方程 · 维度~10³ · 离线仿真/数字孪生', options: { fontSize: F.SMALL, color: C.WHITE } },
  ], { x: 1.5, y: 4.7, w: 7.0, h: 1.6, align: 'center', valign: 'middle', margin: 0 });

  // SM middle
  s.addShape(pres.shapes.TRAPEZOID, {
    x: 1.8, y: 2.7, w: 6.4, h: 1.7,
    fill: { color: C.LBLUE }, line: { color: C.WHITE, width: 2 },
    rotate: 180,
  });
  s.addText([
    { text: 'SM 简化模型', options: { fontSize: 20, bold: true, color: C.WHITE, breakLine: true } },
    { text: 'Simplified Model (IDZ)', options: { fontSize: F.BOX_SUB, color: C.WHITE, breakLine: true } },
    { text: '维度~10¹ · 在线MPC优化控制', options: { fontSize: F.SMALL, color: C.WHITE } },
  ], { x: 2.3, y: 2.8, w: 5.4, h: 1.5, align: 'center', valign: 'middle', margin: 0 });

  // OSEM top
  s.addShape(pres.shapes.TRAPEZOID, {
    x: 2.8, y: 1.1, w: 4.4, h: 1.4,
    fill: { color: C.XLBLUE }, line: { color: C.WHITE, width: 2 },
    rotate: 180,
  });
  s.addText([
    { text: 'OSEM 观测与状态估计模型', options: { fontSize: 18, bold: true, color: '0D47A1', breakLine: true } },
    { text: 'Observation & State Estimation', options: { fontSize: 11, color: C.BLUE, breakLine: true } },
    { text: '参数校正 · 软测量 · 数据同化', options: { fontSize: F.SMALL, color: C.BLUE } },
  ], { x: 3.0, y: 1.15, w: 4.0, h: 1.3, align: 'center', valign: 'middle', margin: 0 });

  // Left axis
  s.addText('物理保真度 ↑', { x: -0.1, y: 3.0, w: 0.6, h: 3.0, fontSize: 14, bold: true, color: C.BLUE, rotate: 270, align: 'center', valign: 'middle', margin: 0 });
  // Right axis
  s.addText('计算效率 ↑', { x: 9.5, y: 1.5, w: 0.5, h: 3.0, fontSize: 14, bold: true, color: C.GREEN, rotate: 90, align: 'center', valign: 'middle', margin: 0 });

  // Annotation: 降阶
  s.addText([
    { text: '降阶方法', options: { fontSize: F.LABEL, bold: true, color: C.BLUE, breakLine: true } },
    { text: 'Model Reduction', options: { fontSize: 11, color: C.LBLUE } },
  ], { x: 0.3, y: 3.5, w: 1.5, h: 0.7, margin: 0 });
  s.addShape(pres.shapes.LINE, { x: 1.1, y: 4.2, w: 0.5, h: -0.6, line: { color: C.BLUE, width: 2, endArrowType: 'triangle' } });

  // Annotation: 数据同化
  s.addText([
    { text: '数据同化', options: { fontSize: F.LABEL, bold: true, color: C.LBLUE, breakLine: true } },
    { text: 'Data Assimilation', options: { fontSize: 11, color: C.XLBLUE } },
  ], { x: 7.8, y: 2.0, w: 1.8, h: 0.7, margin: 0 });
  s.addShape(pres.shapes.LINE, { x: 7.6, y: 3.0, w: 0.4, h: -0.5, line: { color: C.LBLUE, width: 2, dashType: 'dash', endArrowType: 'triangle' } });

  // Bottom note
  s.addText('三层模型通过降阶（PBM→SM）和数据同化（SM↔OSEM）形成闭环协作', {
    x: 0.5, y: 6.7, w: 9.0, h: 0.4, fontSize: F.NOTE, color: C.GRAY, align: 'center', margin: 0,
  });
}

// ========== Slide 3: 图6-4 xIL矩阵 ==========
function slide_06_04(pres) {
  let s = pres.addSlide();
  s.background = { color: C.WHITE };

  s.addText([
    { text: '图 6-4　在环验证深度与WNAL等级对应', options: { fontSize: F.TITLE, bold: true, color: C.TEXT, breakLine: true } },
    { text: 'Fig. 6-4 xIL Verification Depth vs. WNAL Level', options: { fontSize: F.SUBTITLE, color: C.GRAY } },
  ], { x: 0.3, y: 0.15, w: 9.4, h: 0.8, align: 'center', valign: 'top' });

  const rows = [
    { label: 'MIL', labelCn: '模型在环', data: [0, 1, 2, 2, 2, 2] },
    { label: 'SIL', labelCn: '软件在环', data: [0, 0, 1, 2, 2, 2] },
    { label: 'HIL', labelCn: '硬件在环', data: [0, 0, 0, 1, 2, 2] },
  ];
  const cols = ['L0', 'L1', 'L2', 'L3', 'L4', 'L5'];
  const cellW = 1.15, cellH = 1.3;
  const startX = 2.4, startY = 1.3;
  const fills = { 0: C.XLGRAY, 1: C.XXLBLUE, 2: C.BLUE };
  const texts = { 0: '—', 1: '推荐', 2: '必须' };
  const textsEn = { 0: '', 1: 'Recom.', 2: 'Required' };
  const textColors = { 0: 'BDBDBD', 1: C.BLUE, 2: C.WHITE };

  // Column headers
  cols.forEach((col, j) => {
    const isL3 = j === 3;
    s.addText(col, {
      x: startX + j * cellW, y: startY - 0.5, w: cellW, h: 0.45,
      fontSize: F.HEADER, bold: true, color: isL3 ? C.DKRED : C.TEXT, align: 'center', valign: 'bottom', margin: 0,
    });
  });

  // Row labels
  rows.forEach((row, i) => {
    s.addText([
      { text: row.label, options: { fontSize: F.BOX_MAIN, bold: true, color: C.TEXT, breakLine: true } },
      { text: row.labelCn, options: { fontSize: F.SMALL, color: C.GRAY } },
    ], { x: 0.3, y: startY + i * cellH + 0.1, w: 2.0, h: cellH - 0.2, align: 'right', valign: 'middle', margin: 0 });
  });

  // Cells
  rows.forEach((row, i) => {
    row.data.forEach((val, j) => {
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
        x: startX + j * cellW + 0.04, y: startY + i * cellH + 0.04,
        w: cellW - 0.08, h: cellH - 0.08,
        fill: { color: fills[val] }, rectRadius: 0.06,
        line: val > 0 ? { color: val === 2 ? '0D47A1' : C.XLBLUE, width: 1.5 } : { color: C.LGRAY, width: 1 },
      });
      const textArr = [{ text: texts[val], options: { fontSize: F.CELL, bold: true, color: textColors[val] } }];
      if (textsEn[val]) {
        textArr[0].options.breakLine = true;
        textArr.push({ text: textsEn[val], options: { fontSize: 10, color: val === 2 ? C.WHITE : C.LBLUE } });
      }
      s.addText(textArr, {
        x: startX + j * cellW + 0.04, y: startY + i * cellH + 0.04,
        w: cellW - 0.08, h: cellH - 0.08,
        align: 'center', valign: 'middle', margin: 0,
      });
    });
  });

  // Red threshold line
  const lineX = startX + 3 * cellW;
  s.addShape(pres.shapes.LINE, {
    x: lineX, y: startY - 0.4, w: 0, h: 3 * cellH + 0.7,
    line: { color: C.RED, width: 3, dashType: 'lgDash' },
  });
  s.addText([
    { text: '← L2 / L3 质变节点 →', options: { fontSize: F.LABEL, bold: true, color: C.DKRED, breakLine: true } },
    { text: 'Critical Threshold', options: { fontSize: F.SMALL, color: C.RED } },
  ], { x: lineX - 2.0, y: startY + 3 * cellH + 0.45, w: 4.0, h: 0.6, align: 'center', valign: 'top', margin: 0 });

  // Legend
  const legY = 6.2;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 1.0, y: legY, w: 0.3, h: 0.22, fill: { color: C.BLUE }, rectRadius: 0.03 });
  s.addText('必须 Required', { x: 1.4, y: legY - 0.03, w: 2.0, h: 0.3, fontSize: F.LEGEND, color: C.TEXT, margin: 0 });

  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 3.6, y: legY, w: 0.3, h: 0.22, fill: { color: C.XXLBLUE }, line: { color: C.XLBLUE, width: 1 }, rectRadius: 0.03 });
  s.addText('推荐 Recommended', { x: 4.0, y: legY - 0.03, w: 2.5, h: 0.3, fontSize: F.LEGEND, color: C.TEXT, margin: 0 });

  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 6.8, y: legY, w: 0.3, h: 0.22, fill: { color: C.XLGRAY }, line: { color: C.LGRAY, width: 1 }, rectRadius: 0.03 });
  s.addText('不要求 N/A', { x: 7.2, y: legY - 0.03, w: 2.0, h: 0.3, fontSize: F.LEGEND, color: C.TEXT, margin: 0 });
}

// ========== Slide 4: 图7-1 WNAL阶梯 ==========
function slide_07_01(pres) {
  let s = pres.addSlide();
  s.background = { color: C.WHITE };

  s.addText([
    { text: '图 7-1　WNAL水网自主等级阶梯图', options: { fontSize: F.TITLE, bold: true, color: C.TEXT, breakLine: true } },
    { text: 'Fig. 7-1 WNAL L0-L5 Water Network Autonomy Ladder', options: { fontSize: F.SUBTITLE, color: C.GRAY } },
  ], { x: 0.3, y: 0.15, w: 9.4, h: 0.8, align: 'center', valign: 'top' });

  const levels = [
    { label: 'L0', name: '手动运行', nameEn: 'Manual', color: 'BDBDBD', h: 1.5, desc: '人工观测\n经验决策' },
    { label: 'L1', name: '规则自动化', nameEn: 'Rule-Based', color: C.XLBLUE, h: 2.1, desc: '固定规则\n自动执行' },
    { label: 'L2', name: '模型优化', nameEn: 'Model-Based', color: C.LBLUE, h: 2.8, desc: 'MPC优化\n人工监督' },
    { label: 'L3', name: '条件自主', nameEn: 'Conditional', color: C.BLUE, h: 3.5, desc: 'ODD内自主\n安全降级', special: true, note: '近期目标 3-5年' },
    { label: 'L4', name: '高度自主', nameEn: 'High Auto.', color: '0D47A1', h: 4.2, desc: '扩展ODD\n自诊断', note: '中期 5-10年' },
    { label: 'L5', name: '完全自主', nameEn: 'Full Auto.', color: C.GOLD, h: 4.8, desc: '全工况\n(长期愿景)', dashed: true },
  ];

  const barW = 1.25, gap = 0.2, baseY = 6.0;
  const startX = 0.6;

  levels.forEach((lv, i) => {
    const x = startX + i * (barW + gap);
    const y = baseY - lv.h;

    if (lv.dashed) {
      s.addShape(pres.shapes.RECTANGLE, {
        x: x, y: y, w: barW, h: lv.h,
        fill: { color: C.BGGOLD, transparency: 40 },
        line: { color: C.GOLD, width: 3, dashType: 'lgDash' },
      });
    } else if (lv.special) {
      s.addShape(pres.shapes.RECTANGLE, {
        x: x, y: y, w: barW, h: lv.h,
        fill: { color: lv.color },
        line: { color: C.RED, width: 3 },
      });
    } else {
      s.addShape(pres.shapes.RECTANGLE, {
        x: x, y: y, w: barW, h: lv.h,
        fill: { color: lv.color },
      });
    }

    // Level label
    const txtColor = (lv.dashed) ? C.DKGOLD : C.WHITE;
    s.addText(lv.label, {
      x: x, y: y + 0.08, w: barW, h: 0.45,
      fontSize: 26, bold: true, color: txtColor, align: 'center', valign: 'middle', margin: 0,
    });
    s.addText([
      { text: lv.name, options: { fontSize: F.SMALL, bold: true, color: txtColor, breakLine: true } },
      { text: lv.nameEn, options: { fontSize: 10, color: txtColor } },
    ], { x: x, y: y + 0.55, w: barW, h: 0.5, align: 'center', valign: 'top', margin: 0 });

    // Description below bar
    s.addText(lv.desc, {
      x: x - 0.05, y: baseY + 0.1, w: barW + 0.1, h: 0.65,
      fontSize: 11, color: C.GRAY, align: 'center', valign: 'top', margin: 0,
    });

    // Note
    if (lv.note) {
      s.addText(lv.note, {
        x: x - 0.1, y: baseY + 0.75, w: barW + 0.2, h: 0.3,
        fontSize: 11, bold: true, color: C.BLUE, align: 'center', valign: 'top', margin: 0,
      });
    }
  });

  // Red threshold line between L2 and L3
  const threshX = startX + 3 * (barW + gap) - gap / 2;
  s.addShape(pres.shapes.LINE, {
    x: threshX, y: 1.0, w: 0, h: 5.1,
    line: { color: C.RED, width: 3, dashType: 'lgDash' },
  });
  s.addText([
    { text: '质变节点', options: { fontSize: F.LABEL, bold: true, color: C.DKRED, breakLine: true } },
    { text: 'Critical', options: { fontSize: F.SMALL, color: C.RED } },
  ], { x: threshX - 0.7, y: 1.0, w: 1.4, h: 0.7, align: 'center', valign: 'top', margin: 0 });
}

// ========== Slide 5: 图7-3 八原理×WNAL映射 ==========
function slide_07_03(pres) {
  let s = pres.addSlide();
  s.background = { color: C.WHITE };

  s.addText([
    { text: '图 7-3　CHS八原理与WNAL等级映射', options: { fontSize: F.TITLE, bold: true, color: C.TEXT, breakLine: true } },
    { text: 'Fig. 7-3 Mapping of CHS Eight Principles to WNAL Levels', options: { fontSize: F.SUBTITLE, color: C.GRAY } },
  ], { x: 0.3, y: 0.05, w: 9.4, h: 0.65, align: 'center', valign: 'top' });

  // 8×6 matrix
  const data = [
    [0, 1, 2, 2, 2, 2],  // P1
    [0, 0, 1, 2, 2, 2],  // P2
    [0, 0, 0, 2, 2, 2],  // P3
    [0, 0, 1, 2, 2, 2],  // P4
    [0, 0, 1, 2, 2, 2],  // P5
    [0, 0, 0, 1, 2, 2],  // P6
    [0, 1, 1, 2, 2, 2],  // P7
    [0, 0, 0, 0, 1, 2],  // P8
  ];
  const rowLabels = ['P1 传递函数化', 'P2 可控可观性', 'P3 分层分布式',
                     'P4 安全包络', 'P5 在环验证', 'P6 认知增强',
                     'P7 人机共融', 'P8 自主演进'];
  const rowColors = [C.BLUE, C.BLUE, C.BLUE, C.RED, C.GREEN, C.PURPLE, C.PURPLE, C.GOLD];
  const cols = ['L0', 'L1', 'L2', 'L3', 'L4', 'L5'];

  const cellW = 0.95, cellH = 0.72;
  const startX = 3.2, startY = 1.05;
  const fillMap = { 0: C.XLGRAY, 1: C.XXLBLUE, 2: C.BLUE };
  const symMap = { 0: '○', 1: '◐', 2: '●' };
  const symColor = { 0: 'BDBDBD', 1: C.BLUE, 2: C.WHITE };

  // Column headers
  cols.forEach((col, j) => {
    s.addText(col, {
      x: startX + j * cellW, y: startY - 0.4, w: cellW, h: 0.35,
      fontSize: F.HEADER, bold: true, color: C.TEXT, align: 'center', valign: 'bottom', margin: 0,
    });
  });

  // Row labels + cells
  data.forEach((row, i) => {
    s.addText(rowLabels[i], {
      x: 0.2, y: startY + i * cellH + 0.05, w: 2.9, h: cellH - 0.1,
      fontSize: 14, bold: true, color: rowColors[i], align: 'right', valign: 'middle', margin: 0,
    });
    row.forEach((val, j) => {
      s.addShape(pres.shapes.RECTANGLE, {
        x: startX + j * cellW + 0.03, y: startY + i * cellH + 0.03,
        w: cellW - 0.06, h: cellH - 0.06,
        fill: { color: fillMap[val] },
        line: val > 0 ? { color: val === 2 ? '0D47A1' : C.XLBLUE, width: 1 } : { color: C.LGRAY, width: 0.5 },
      });
      s.addText(symMap[val], {
        x: startX + j * cellW + 0.03, y: startY + i * cellH + 0.03,
        w: cellW - 0.06, h: cellH - 0.06,
        fontSize: 18, color: symColor[val], align: 'center', valign: 'middle', margin: 0,
      });
    });
  });

  // Red threshold line
  const threshX = startX + 3 * cellW;
  s.addShape(pres.shapes.LINE, {
    x: threshX, y: startY - 0.3, w: 0, h: 8 * cellH + 0.5,
    line: { color: C.RED, width: 3, dashType: 'lgDash' },
  });
  s.addText('最小完备集分界', {
    x: threshX - 1.2, y: startY + 8 * cellH + 0.3, w: 2.4, h: 0.3,
    fontSize: F.SMALL, bold: true, color: C.DKRED, align: 'center', margin: 0,
  });

  // Legend
  const legY = startY + 8 * cellH + 0.7;
  s.addShape(pres.shapes.RECTANGLE, { x: 1.0, y: legY, w: 0.25, h: 0.2, fill: { color: C.BLUE } });
  s.addText('● 必须完整实现', { x: 1.3, y: legY - 0.03, w: 2.2, h: 0.3, fontSize: F.LEGEND, color: C.TEXT, margin: 0 });
  s.addShape(pres.shapes.RECTANGLE, { x: 3.8, y: legY, w: 0.25, h: 0.2, fill: { color: C.XXLBLUE }, line: { color: C.XLBLUE, width: 1 } });
  s.addText('◐ 部分/基本形式', { x: 4.1, y: legY - 0.03, w: 2.5, h: 0.3, fontSize: F.LEGEND, color: C.TEXT, margin: 0 });
  s.addShape(pres.shapes.RECTANGLE, { x: 6.8, y: legY, w: 0.25, h: 0.2, fill: { color: C.XLGRAY }, line: { color: C.LGRAY, width: 1 } });
  s.addText('○ 不要求', { x: 7.1, y: legY - 0.03, w: 1.5, h: 0.3, fontSize: F.LEGEND, color: C.TEXT, margin: 0 });
}

// ========== 生成 ==========
async function main() {
  let pres = new pptxgen();
  pres.layout = 'LAYOUT_4x3'; // 10" × 7.5", 更适合学术图
  pres.author = 'Lei Xiaohui';
  pres.title = 'T1-CN 关键插图（可编辑版）';

  slide_01_04(pres);
  slide_02_02(pres);
  slide_06_04(pres);
  slide_07_01(pres);
  slide_07_03(pres);

  const outPath = '/home/claude/T1-CN_figures_editable.pptx';
  await pres.writeFile({ fileName: outPath });
  console.log('✅ Generated:', outPath);
}

main().catch(e => { console.error(e); process.exit(1); });
