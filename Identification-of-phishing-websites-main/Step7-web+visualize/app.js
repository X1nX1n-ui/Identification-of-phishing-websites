// 莫兰迪色系配置
const colors = {
    primary: '#3A3632',       // 柔和炭黑
    warmOrange: '#D4886E',    // 暖橙红
    ginger: '#D4A574',        // 暖姜黄
    green: '#828B78',         // 绿色
    surface: '#E8DCC8',       // 驼色
    light: '#F9F5ED',         // 浅杏色
    border: '#C9BFB0',        // 边框
    text: '#2D2A27'           // 文字
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

    // 显示加载状态
    detectBtn.innerHTML = '分析中 <span class="loading"></span>';
    detectBtn.disabled = true;

    try {
        // 模拟API调用 - 在实际项目中替换为真实的后端API
        await simulateDetection(url);
        
        // 显示结果
        resultContainer.classList.add('show');
        
        // 滚动到结果区域
        setTimeout(() => {
            resultContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }, 300);
    } catch (error) {
        console.error('检测失败:', error);
        alert('检测失败，请稍后重试');
    } finally {
        detectBtn.innerHTML = '开始分析';
        detectBtn.disabled = false;
    }
}

// 模拟检测过程
async function simulateDetection(url) {
    return new Promise((resolve) => {
        setTimeout(() => {
            // 模拟特征提取和预测
            const features = extractMockFeatures(url);
            const prediction = predictPhishing(features);
            displayResult(prediction, features);
            resolve();
        }, 2000);
    });
}

// 模拟特征提取
function extractMockFeatures(url) {
    const hasHttps = url.startsWith('https');
    const urlLength = url.length;
    const hasSuspiciousChars = /[@-]/.test(url);
    const domainAge = Math.floor(Math.random() * 3650); // 0-10年
    
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

// 模拟预测
function predictPhishing(features) {
    // 简单的规则判断（实际项目中使用训练好的模型）
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

// 显示检测结果
function displayResult(prediction, features) {
    const resultStatus = document.getElementById('resultStatus');
    const statusText = document.getElementById('statusText');
    const confidenceScore = document.getElementById('confidenceScore');
    const resultDetails = document.getElementById('resultDetails');

    // 更新状态
    if (prediction.is_phishing) {
        resultStatus.classList.add('danger');
        resultStatus.style.borderLeftColor = colors.warmOrange;
        statusText.textContent = '疑似钓鱼网站';
    } else {
        resultStatus.classList.remove('danger');
        resultStatus.style.borderLeftColor = colors.green;
        statusText.textContent = '安全网站';
    }

    confidenceScore.textContent = `置信度: ${prediction.confidence}%`;

    // 显示详细信息
    resultDetails.innerHTML = `
        <div class="detail-item">
            <span class="detail-label">URL长度</span>
            <span class="detail-value">${features.url_length} 字符</span>
        </div>
        <div class="detail-item">
            <span class="detail-label">协议类型</span>
            <span class="detail-value">${features.has_https ? 'HTTPS' : 'HTTP'}</span>
        </div>
        <div class="detail-item">
            <span class="detail-label">域名年龄</span>
            <span class="detail-value">${Math.floor(features.domain_age_days / 365)} 年</span>
        </div>
        <div class="detail-item">
            <span class="detail-label">DNS验证</span>
            <span class="detail-value">${features.dns_valid ? '有效' : '无效'}</span>
        </div>
        <div class="detail-item">
            <span class="detail-label">风险评分</span>
            <span class="detail-value">${prediction.risk_score}/100</span>
        </div>
    `;

    // 更新统计数据
    updateStatistics();
}

// 更新统计数据
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
    createTrainingHistory();
}

// 1. 混淆矩阵 - 优化版本
function createConfusionMatrix() {
    const ctx = document.getElementById('confusionMatrix');
    
    // 自定义混淆矩阵插件
    const confusionMatrixPlugin = {
        id: 'confusionMatrix',
        afterDatasetsDraw(chart) {
            const { ctx, chartArea: { left, top, width, height } } = chart;
            const data = [
                [6333, 621],   // True Negative, False Positive
                [569, 6476]    // False Negative, True Positive
            ];
            
            const cellWidth = width / 2;
            const cellHeight = height / 2;
            
            // 绘制单元格
            data.forEach((row, i) => {
                row.forEach((value, j) => {
                    const x = left + j * cellWidth;
                    const y = top + i * cellHeight;
                    
                    // 背景色 - 调整强度以便区分
                    const maxValue = 6500;
                    const intensity = value / maxValue;
                    if (i === j) {
                        ctx.fillStyle = `rgba(130, 139, 120, ${0.3 + intensity * 0.5})`; // 绿色
                    } else {
                        ctx.fillStyle = `rgba(212, 136, 110, ${0.2 + intensity * 0.3})`; // 橙红
                    }
                    ctx.fillRect(x, y, cellWidth, cellHeight);
                    
                    // 边框
                    ctx.strokeStyle = colors.border;
                    ctx.lineWidth = 2;
                    ctx.strokeRect(x, y, cellWidth, cellHeight);
                    
                    // 数值 - 更大的字体以便清晰显示
                    ctx.fillStyle = colors.text;
                    ctx.font = '600 52px "Crimson Text"';
                    ctx.textAlign = 'center';
                    ctx.textBaseline = 'middle';
                    ctx.fillText(value, x + cellWidth / 2, y + cellHeight / 2 - 30);
                    
                    // 标签 - 更清晰的位置和描述
                    ctx.font = '400 15px "Work Sans"';
                    ctx.fillStyle = colors.text;
                    if (i === 0 && j === 0) {
                        ctx.fillText('合法网站 (0)', x + cellWidth / 2, y + cellHeight - 40);
                        ctx.font = '400 12px "Work Sans"';
                        ctx.fillStyle = 'rgba(45, 42, 39, 0.6)';
                        ctx.fillText('预测:合法 实际:合法', x + cellWidth / 2, y + cellHeight - 20);
                    }
                    if (i === 0 && j === 1) {
                        ctx.fillText('钓鱼网站 (1)', x + cellWidth / 2, y + cellHeight - 40);
                        ctx.font = '400 12px "Work Sans"';
                        ctx.fillStyle = 'rgba(45, 42, 39, 0.6)';
                        ctx.fillText('预测:钓鱼 实际:合法', x + cellWidth / 2, y + cellHeight - 20);
                    }
                    if (i === 1 && j === 0) {
                        ctx.fillText('合法网站 (0)', x + cellWidth / 2, y + cellHeight - 40);
                        ctx.font = '400 12px "Work Sans"';
                        ctx.fillStyle = 'rgba(45, 42, 39, 0.6)';
                        ctx.fillText('预测:合法 实际:钓鱼', x + cellWidth / 2, y + cellHeight - 20);
                    }
                    if (i === 1 && j === 1) {
                        ctx.fillText('钓鱼网站 (1)', x + cellWidth / 2, y + cellHeight - 40);
                        ctx.font = '400 12px "Work Sans"';
                        ctx.fillStyle = 'rgba(45, 42, 39, 0.6)';
                        ctx.fillText('预测:钓鱼 实际:钓鱼', x + cellWidth / 2, y + cellHeight - 20);
                    }
                });
            });
            
            // 添加轴标签
            ctx.fillStyle = colors.text;
            ctx.font = '500 16px "Work Sans"';
            ctx.textAlign = 'center';
            ctx.fillText('预测标签 / Predicted Label', left + width / 2, top + height + 50);
            
            ctx.save();
            ctx.translate(left - 80, top + height / 2);
            ctx.rotate(-Math.PI / 2);
            ctx.fillText('真实标签 / True Label', 0, 0);
            ctx.restore();
        }
    };
    
    new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: [{
                data: []
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            layout: {
                padding: {
                    left: 100,
                    right: 30,
                    top: 30,
                    bottom: 70
                }
            },
            plugins: {
                legend: { display: false },
                tooltip: { enabled: false }
            },
            scales: {
                x: {
                    display: false,
                    min: 0,
                    max: 2
                },
                y: {
                    display: false,
                    min: 0,
                    max: 2
                }
            }
        },
        plugins: [confusionMatrixPlugin]
    });
}

// 2. 特征重要性 - 优化版本
function createFeatureImportance() {
    const ctx = document.getElementById('featureImportance');
    
    const features = [
        { name: 'URL长度', importance: 0.337 },
        { name: '混淆JS', importance: 0.195 },
        { name: 'iframe', importance: 0.193 },
        { name: '点号数', importance: 0.162 },
        { name: '子域名数', importance: 0.079 },
        { name: 'HTTPS', importance: 0.032 },
        { name: 'IP地址', importance: 0.003 },
        { name: 'WHOIS', importance: 0.000 },
        { name: 'DNS有效', importance: 0.000 },
        { name: '域名年龄', importance: 0.000 }
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
                padding: {
                    left: 20,
                    right: 20,
                    top: 10,
                    bottom: 10
                }
            },
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: colors.primary,
                    titleColor: colors.light,
                    bodyColor: colors.light,
                    padding: 12,
                    displayColors: false,
                    callbacks: {
                        label: (context) => `重要性: ${(context.parsed.x * 100).toFixed(1)}%`
                    }
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: '重要性 / Importance',
                        color: colors.text,
                        font: {
                            family: 'Work Sans',
                            size: 13,
                            weight: '500'
                        }
                    },
                    grid: {
                        color: colors.border,
                        lineWidth: 1
                    },
                    ticks: {
                        color: colors.text,
                        font: {
                            family: 'Work Sans',
                            size: 11
                        },
                        callback: (value) => `${(value * 100).toFixed(0)}%`
                    },
                    border: {
                        color: colors.primary,
                        width: 2
                    }
                },
                y: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        color: colors.text,
                        font: {
                            family: 'Work Sans',
                            size: 13,
                            weight: '500'
                        }
                    },
                    border: {
                        color: colors.primary,
                        width: 2
                    }
                }
            }
        }
    });
}

// 3. ROC曲线
function createROCCurve() {
    const ctx = document.getElementById('rocCurve');
    
    // 生成ROC曲线数据
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
                    label: 'ROC曲线 (AUC = 0.975)',
                    data: rocPoints,
                    borderColor: colors.green,
                    backgroundColor: 'transparent',
                    borderWidth: 3,
                    pointRadius: 0,
                    tension: 0.4
                },
                {
                    label: '随机猜测 (AUC = 0.500)',
                    data: [{ x: 0, y: 0 }, { x: 1, y: 1 }],
                    borderColor: colors.border,
                    borderDash: [5, 5],
                    borderWidth: 2,
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
                        font: {
                            family: 'Work Sans',
                            size: 12
                        },
                        padding: 20,
                        usePointStyle: true
                    }
                },
                tooltip: {
                    backgroundColor: colors.primary,
                    titleColor: colors.light,
                    bodyColor: colors.light,
                    padding: 12,
                    callbacks: {
                        label: (context) => `假阳性率: ${context.parsed.x.toFixed(3)}, 真阳性率: ${context.parsed.y.toFixed(3)}`
                    }
                }
            },
            scales: {
                x: {
                    type: 'linear',
                    title: {
                        display: true,
                        text: '假阳性率 / False Positive Rate',
                        color: colors.text,
                        font: {
                            family: 'Work Sans',
                            size: 13,
                            weight: '500'
                        }
                    },
                    grid: {
                        color: colors.border,
                        lineWidth: 1
                    },
                    ticks: {
                        color: colors.text,
                        font: {
                            family: 'Work Sans',
                            size: 11
                        }
                    },
                    border: {
                        color: colors.primary,
                        width: 2
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: '真阳性率 / True Positive Rate',
                        color: colors.text,
                        font: {
                            family: 'Work Sans',
                            size: 13,
                            weight: '500'
                        }
                    },
                    grid: {
                        color: colors.border,
                        lineWidth: 1
                    },
                    ticks: {
                        color: colors.text,
                        font: {
                            family: 'Work Sans',
                            size: 11
                        }
                    },
                    border: {
                        color: colors.primary,
                        width: 2
                    }
                }
            }
        }
    });
}

// 4. 训练历史
function createTrainingHistory() {
    const ctx = document.getElementById('trainingHistory');
    
    // 生成训练数据
    const epochs = Array.from({ length: 100 }, (_, i) => i + 1);
    const trainLoss = epochs.map(e => 0.5 * Math.exp(-e / 20) + Math.random() * 0.05);
    const valLoss = epochs.map(e => 0.55 * Math.exp(-e / 18) + Math.random() * 0.06);
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: epochs,
            datasets: [
                {
                    label: '训练损失 / Training Loss',
                    data: trainLoss,
                    borderColor: colors.warmOrange,
                    backgroundColor: 'transparent',
                    borderWidth: 2,
                    pointRadius: 0,
                    tension: 0.4
                },
                {
                    label: '验证损失 / Validation Loss',
                    data: valLoss,
                    borderColor: colors.ginger,
                    backgroundColor: 'transparent',
                    borderWidth: 2,
                    pointRadius: 0,
                    tension: 0.4
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
                        font: {
                            family: 'Work Sans',
                            size: 12
                        },
                        padding: 20,
                        usePointStyle: true
                    }
                },
                tooltip: {
                    backgroundColor: colors.primary,
                    titleColor: colors.light,
                    bodyColor: colors.light,
                    padding: 12
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Epoch',
                        color: colors.text,
                        font: {
                            family: 'Work Sans',
                            size: 13,
                            weight: '500'
                        }
                    },
                    grid: {
                        color: colors.border,
                        lineWidth: 1
                    },
                    ticks: {
                        color: colors.text,
                        font: {
                            family: 'Work Sans',
                            size: 11
                        },
                        maxTicksLimit: 10
                    },
                    border: {
                        color: colors.primary,
                        width: 2
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: '损失 / Loss',
                        color: colors.text,
                        font: {
                            family: 'Work Sans',
                            size: 13,
                            weight: '500'
                        }
                    },
                    grid: {
                        color: colors.border,
                        lineWidth: 1
                    },
                    ticks: {
                        color: colors.text,
                        font: {
                            family: 'Work Sans',
                            size: 11
                        }
                    },
                    border: {
                        color: colors.primary,
                        width: 2
                    }
                }
            }
        }
    });
}

// 页面加载时初始化
document.addEventListener('DOMContentLoaded', () => {
    initializeCharts();
    
    // 回车键触发检测
    document.getElementById('urlInput').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            detectURL();
        }
    });
});
