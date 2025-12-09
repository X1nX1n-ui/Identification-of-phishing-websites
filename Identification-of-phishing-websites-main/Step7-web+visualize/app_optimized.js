// 莫兰迪色系配置
const colors = {
    primary: '#3A3632',
    warmOrange: '#D4886E',
    ginger: '#D4A574',
    green: '#828B78',
    surface: '#E8DCC8',
    light: '#F9F5ED',
    border: '#C9BFB0',
    text: '#2D2A27'
};

// URL检测功能
async function detectURL() {
    const urlInput = document.getElementById('urlInput');
    const detectBtn = document.getElementById('detectBtn');
    const resultContainer = document.getElementById('resultContainer');
    const url = urlInput.value.trim();

    if (!url) {
        alert('请输入URL地址');
        return;
    }

    detectBtn.innerHTML = '分析中 <span class="loading"></span>';
    detectBtn.disabled = true;

    try {
        await simulateDetection(url);
        resultContainer.classList.add('show');
    } catch (error) {
        console.error('检测失败:', error);
        alert('检测失败，请稍后重试');
    } finally {
        detectBtn.innerHTML = '开始分析';
        detectBtn.disabled = false;
    }
}

async function simulateDetection(url) {
    return new Promise((resolve) => {
        setTimeout(() => {
            const features = extractMockFeatures(url);
            const prediction = predictPhishing(features);
            displayResult(prediction, features);
            resolve();
        }, 1500);
    });
}

function extractMockFeatures(url) {
    const hasHttps = url.startsWith('https');
    const urlLength = url.length;
    const hasSuspiciousChars = /[@-]/.test(url);
    const domainAge = Math.floor(Math.random() * 3650);
    
    return {
        url_length: urlLength,
        protocol: hasHttps ? 1 : 0,
        num_dots: (url.match(/\./g) || []).length,
        has_suspicious: hasSuspiciousChars ? 1 : 0,
        domain_age_days: domainAge,
        has_https: hasHttps,
        dns_valid: Math.random() > 0.1 ? 1 : 0
    };
}

function predictPhishing(features) {
    let score = 0;
    if (features.protocol === 0) score += 30;
    if (features.url_length > 75) score += 20;
    if (features.has_suspicious) score += 25;
    if (features.domain_age_days < 365) score += 15;
    if (features.dns_valid === 0) score += 10;
    
    const confidence = score > 50 ? score : 100 - score;
    const isPhishing = score > 50;
    
    return {
        is_phishing: isPhishing,
        confidence: confidence.toFixed(1),
        risk_score: score,
        features: features
    };
}

function displayResult(prediction, features) {
    const resultHeader = document.getElementById('resultHeader');
    const resultInfo = document.getElementById('resultInfo');

    if (prediction.is_phishing) {
        resultHeader.textContent = '⚠️ 疑似钓鱼网站';
        resultHeader.style.color = colors.warmOrange;
    } else {
        resultHeader.textContent = '✓ 安全网站';
        resultHeader.style.color = colors.green;
    }

    resultInfo.innerHTML = `
        <div class="result-item">
            状态: <span class="result-value">${prediction.is_phishing ? '危险' : '安全'}</span>
        </div>
        <div class="result-item">
            置信度: <span class="result-value">${prediction.confidence}%</span>
        </div>
        <div class="result-item">
            风险评分: <span class="result-value">${prediction.risk_score}/100</span>
        </div>
        <div class="result-item">
            协议: <span class="result-value">${features.has_https ? 'HTTPS' : 'HTTP'}</span>
        </div>
    `;

    updateStatistics();
}

function updateStatistics() {
    const totalScans = document.getElementById('totalScans');
    const current = parseInt(totalScans.textContent.replace(',', ''));
    totalScans.textContent = (current + 1).toLocaleString();
}

// 初始化图表
function initializeCharts() {
    createConfusionMatrix();
    createFeatureImportance();
    createROCCurve();
    createPerformanceMetrics();
}

// 1. 混淆矩阵 - 紧凑版
function createConfusionMatrix() {
    const ctx = document.getElementById('confusionMatrix');
    
    const confusionMatrixPlugin = {
        id: 'confusionMatrix',
        afterDatasetsDraw(chart) {
            const { ctx, chartArea: { left, top, width, height } } = chart;
            const data = [
                [6333, 621],
                [569, 6476]
            ];
            
            const cellWidth = width / 2;
            const cellHeight = height / 2;
            
            data.forEach((row, i) => {
                row.forEach((value, j) => {
                    const x = left + j * cellWidth;
                    const y = top + i * cellHeight;
                    
                    const maxValue = 6500;
                    const intensity = value / maxValue;
                    if (i === j) {
                        ctx.fillStyle = `rgba(130, 139, 120, ${0.3 + intensity * 0.5})`;
                    } else {
                        ctx.fillStyle = `rgba(212, 136, 110, ${0.2 + intensity * 0.3})`;
                    }
                    ctx.fillRect(x, y, cellWidth, cellHeight);
                    
                    ctx.strokeStyle = colors.border;
                    ctx.lineWidth = 2;
                    ctx.strokeRect(x, y, cellWidth, cellHeight);
                    
                    // 数值
                    ctx.fillStyle = colors.text;
                    ctx.font = '600 32px "Crimson Text"';
                    ctx.textAlign = 'center';
                    ctx.textBaseline = 'middle';
                    ctx.fillText(value, x + cellWidth / 2, y + cellHeight / 2 - 15);
                    
                    // 标签
                    ctx.font = '400 11px "Work Sans"';
                    ctx.fillStyle = 'rgba(45, 42, 39, 0.6)';
                    if (i === 0 && j === 0) ctx.fillText('TN', x + cellWidth / 2, y + cellHeight - 15);
                    if (i === 0 && j === 1) ctx.fillText('FP', x + cellWidth / 2, y + cellHeight - 15);
                    if (i === 1 && j === 0) ctx.fillText('FN', x + cellWidth / 2, y + cellHeight - 15);
                    if (i === 1 && j === 1) ctx.fillText('TP', x + cellWidth / 2, y + cellHeight - 15);
                });
            });
            
            // 轴标签
            ctx.fillStyle = colors.text;
            ctx.font = '500 12px "Work Sans"';
            ctx.textAlign = 'center';
            ctx.fillText('预测 / Predicted', left + width / 2, top + height + 35);
            
            ctx.save();
            ctx.translate(left - 50, top + height / 2);
            ctx.rotate(-Math.PI / 2);
            ctx.fillText('实际 / Actual', 0, 0);
            ctx.restore();
        }
    };
    
    new Chart(ctx, {
        type: 'scatter',
        data: { datasets: [{ data: [] }] },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            layout: {
                padding: { left: 60, right: 20, top: 20, bottom: 45 }
            },
            plugins: {
                legend: { display: false },
                tooltip: { enabled: false }
            },
            scales: {
                x: { display: false },
                y: { display: false }
            }
        },
        plugins: [confusionMatrixPlugin]
    });
}

// 2. 特征重要性 - 紧凑版（只显示Top 7）
function createFeatureImportance() {
    const ctx = document.getElementById('featureImportance');
    
    const features = [
        { name: 'URL长度', importance: 0.337 },
        { name: '混淆JS', importance: 0.195 },
        { name: 'iframe', importance: 0.193 },
        { name: '点号数', importance: 0.162 },
        { name: '子域名数', importance: 0.079 },
        { name: 'HTTPS', importance: 0.032 },
        { name: 'IP地址', importance: 0.003 }
    ];
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: features.map(f => f.name),
            datasets: [{
                data: features.map(f => f.importance),
                backgroundColor: colors.ginger,
                borderColor: colors.primary,
                borderWidth: 2
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            layout: {
                padding: { left: 10, right: 10, top: 5, bottom: 5 }
            },
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: colors.primary,
                    titleColor: colors.light,
                    bodyColor: colors.light,
                    padding: 10,
                    displayColors: false,
                    callbacks: {
                        label: (context) => `${(context.parsed.x * 100).toFixed(1)}%`
                    }
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: '重要性',
                        color: colors.text,
                        font: { family: 'Work Sans', size: 11, weight: '500' }
                    },
                    grid: { color: colors.border, lineWidth: 1 },
                    ticks: {
                        color: colors.text,
                        font: { family: 'Work Sans', size: 10 },
                        callback: (value) => `${(value * 100).toFixed(0)}%`
                    },
                    border: { color: colors.primary, width: 2 }
                },
                y: {
                    grid: { display: false },
                    ticks: {
                        color: colors.text,
                        font: { family: 'Work Sans', size: 11, weight: '500' }
                    },
                    border: { color: colors.primary, width: 2 }
                }
            }
        }
    });
}

// 3. ROC曲线 - 紧凑版
function createROCCurve() {
    const ctx = document.getElementById('rocCurve');
    
    const rocPoints = [];
    for (let i = 0; i <= 100; i++) {
        const fpr = i / 100;
        const tpr = Math.sqrt(fpr) * 0.95 + Math.random() * 0.05;
        rocPoints.push({ x: fpr, y: Math.min(tpr, 1) });
    }
    
    new Chart(ctx, {
        type: 'line',
        data: {
            datasets: [
                {
                    label: 'ROC曲线',
                    data: rocPoints,
                    borderColor: colors.green,
                    backgroundColor: 'transparent',
                    borderWidth: 2.5,
                    pointRadius: 0,
                    tension: 0.4
                },
                {
                    label: '随机',
                    data: [{ x: 0, y: 0 }, { x: 1, y: 1 }],
                    borderColor: colors.border,
                    borderDash: [5, 5],
                    borderWidth: 1.5,
                    pointRadius: 0
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'bottom',
                    labels: {
                        color: colors.text,
                        font: { family: 'Work Sans', size: 10 },
                        padding: 12,
                        usePointStyle: true
                    }
                },
                tooltip: {
                    backgroundColor: colors.primary,
                    padding: 8,
                    callbacks: {
                        label: (ctx) => `FPR: ${ctx.parsed.x.toFixed(2)}, TPR: ${ctx.parsed.y.toFixed(2)}`
                    }
                }
            },
            scales: {
                x: {
                    type: 'linear',
                    title: {
                        display: true,
                        text: '假阳性率 FPR',
                        color: colors.text,
                        font: { family: 'Work Sans', size: 10, weight: '500' }
                    },
                    grid: { color: colors.border, lineWidth: 1 },
                    ticks: {
                        color: colors.text,
                        font: { family: 'Work Sans', size: 9 }
                    },
                    border: { color: colors.primary, width: 2 }
                },
                y: {
                    title: {
                        display: true,
                        text: '真阳性率 TPR',
                        color: colors.text,
                        font: { family: 'Work Sans', size: 10, weight: '500' }
                    },
                    grid: { color: colors.border, lineWidth: 1 },
                    ticks: {
                        color: colors.text,
                        font: { family: 'Work Sans', size: 9 }
                    },
                    border: { color: colors.primary, width: 2 }
                }
            }
        }
    });
}

// 4. 性能指标 - 柱状图
function createPerformanceMetrics() {
    const ctx = document.getElementById('performanceMetrics');
    
    const metrics = [
        { name: '准确率', value: 0.9150 },
        { name: '精确率', value: 0.9125 },
        { name: '召回率', value: 0.9192 },
        { name: 'F1分数', value: 0.9159 }
    ];
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: metrics.map(m => m.name),
            datasets: [{
                data: metrics.map(m => m.value),
                backgroundColor: [
                    colors.green,
                    colors.ginger,
                    colors.warmOrange,
                    colors.primary
                ],
                borderColor: colors.primary,
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: colors.primary,
                    padding: 10,
                    callbacks: {
                        label: (context) => `${(context.parsed.y * 100).toFixed(2)}%`
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 1,
                    title: {
                        display: true,
                        text: '分数',
                        color: colors.text,
                        font: { family: 'Work Sans', size: 11, weight: '500' }
                    },
                    grid: { color: colors.border, lineWidth: 1 },
                    ticks: {
                        color: colors.text,
                        font: { family: 'Work Sans', size: 10 },
                        callback: (value) => `${(value * 100).toFixed(0)}%`
                    },
                    border: { color: colors.primary, width: 2 }
                },
                x: {
                    grid: { display: false },
                    ticks: {
                        color: colors.text,
                        font: { family: 'Work Sans', size: 11, weight: '500' }
                    },
                    border: { color: colors.primary, width: 2 }
                }
            }
        }
    });
}

// 页面加载时初始化
document.addEventListener('DOMContentLoaded', () => {
    initializeCharts();
    
    document.getElementById('urlInput').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            detectURL();
        }
    });
});
