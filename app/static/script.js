
let temperatureChart = null;
let currentIndicator = 'temperature';
let measurementsCache = [];

const indicators = {
    temperature: {
        label: 'Temperatura (°C)',
        color: '#278451',
        background: 'rgba(39, 132, 81, 0.12)'
    },
    humidity: {
        label: 'Umidade (%)',
        color: '#3186c7',
        background: 'rgba(49, 134, 199, 0.12)'
    },
    air_quality: {
        label: 'Qualidade do ar (EAQI)',
        color: '#d59a32',
        background: 'rgba(213, 154, 50, 0.12)'
    }
};

// CLASSIFICAÇÃO DO ÍNDICE EUROPEU DE QUALIDADE DO AR
function classifyAirQuality(value) {
    const index = Number(value);

    if (value === null || value === undefined ||
        value === '' || !Number.isFinite(index) || index < 0) {
        return {
            label: 'Não disponível',
            color: '#777777'
        };
    }

    if (index <= 20) {
        return { label: 'Boa', color: '#168447' };
    }

    if (index <= 40) {
        return { label: 'Razoável', color: '#70a83b' };
    }

    if (index <= 60) {
        return { label: 'Moderada', color: '#c99a19' };
    }

    if (index <= 80) {
        return { label: 'Ruim', color: '#df791c' };
    }

    if (index <= 100) {
        return { label: 'Muito ruim', color: '#d33c40' };
    }

    return {
        label: 'Extremamente ruim',
        color: '#823b94'
    };
}

// ATUALIZAÇÃO DOS CARDS
function updateCard(id, value, unit) {
    const element = document.getElementById(id);

    if (!element) return;

    element.textContent =
        value !== null && value !== undefined
            ? `${value} ${unit}`
            : 'Não disponível';
}

// EXIBIÇÃO DA CLASSIFICAÇÃO
function updateAirQualityClassification(value) {
    const cardValue = document.getElementById('air-quality');

    if (!cardValue) return;

    const classification = classifyAirQuality(value);

    let label = document.getElementById('air-quality-status');

    if (!label) {
        label = document.createElement('p');
        label.id = 'air-quality-status';
        label.style.marginTop = '10px';
        label.style.fontSize = '15px';
        label.style.fontWeight = '700';

        cardValue.insertAdjacentElement('afterend', label);
    }

    label.textContent = classification.label;
    label.style.color = classification.color;
}

// CONSULTA METEOROLÓGICA
async function loadWeather() {
    try {
        const response = await fetch('/weather');

        if (!response.ok) {
            throw new Error('Erro ao consultar dados meteorológicos');
        }

        const weather = await response.json();

        updateCard('temperature', weather.temperature, '°C');
        updateCard('humidity', weather.humidity, '%');

        console.log('Dados meteorológicos reais:', weather);

    } catch (error) {
        console.error('Erro ao carregar clima:', error);

        updateCard('temperature', null, '°C');
        updateCard('humidity', null, '%');
    }
}

// CONSULTA DA QUALIDADE DO AR
async function loadAirQuality() {
    try {
        const response = await fetch('/air-quality');

        if (!response.ok) {
            throw new Error('Erro ao consultar qualidade do ar');
        }

        const data = await response.json();

        const quality =
            data.air_quality ?? data.qualidade_do_ar ?? null;

        updateCard('air-quality', quality, 'EAQI');
        updateAirQualityClassification(quality);

        console.log('Qualidade do ar real:', data);

    } catch (error) {
        console.error('Erro ao carregar qualidade do ar:', error);

        updateCard('air-quality', null, 'EAQI');
        updateAirQualityClassification(null);
    }
}

// FORMATAÇÃO DAS DATAS
function formatDate(value) {
    if (!value) return '-';

    const date = new Date(
        String(value).replace(' ', 'T')
    );

    if (Number.isNaN(date.getTime())) {
        return value;
    }

    return date.toLocaleString('pt-BR');
}

// GRÁFICOS INTERATIVOS
function renderTemperatureChart(measurements) {
    const canvas = document.getElementById('temperature-chart');

    if (!canvas || typeof Chart === 'undefined') return;

    const indicator = indicators[currentIndicator];
    const context = canvas.getContext('2d');

    if (temperatureChart) {
        temperatureChart.destroy();
    }

    const orderedMeasurements = [...measurements].sort(
        (a, b) => new Date(a.measured_at) - new Date(b.measured_at)
    );

    const values = orderedMeasurements.map(item => {
        const value = item[currentIndicator];

        if (value === null || value === undefined || value === '') {
            return null;
        }

        const number = Number(value);

        return Number.isFinite(number) ? number : null;
    });

    temperatureChart = new Chart(context, {
        type: 'line',

        data: {
            labels: orderedMeasurements.map(item =>
                formatDate(item.measured_at)
            ),

            datasets: [{
                label: indicator.label,
                data: values,
                borderColor: indicator.color,
                backgroundColor: indicator.background,
                borderWidth: 3,
                fill: true,
                tension: 0.35,
                spanGaps: false,
                pointRadius: 4,
                pointHoverRadius: 6
            }]
        },

        options: {
            responsive: true,
            maintainAspectRatio: false,

            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    enabled: true
                }
            },

            scales: {
                y: {
                    beginAtZero: false
                }
            }
        }
    });
}

// HISTÓRICO DE MEDIÇÕES
async function loadWeatherHistory() {
    const history = document.getElementById('measurements');

    try {
        const response = await fetch('/weather/history');

        if (!response.ok) {
            throw new Error('Erro ao consultar histórico meteorológico');
        }

        const measurements = await response.json();

        if (!Array.isArray(measurements)) {
            throw new Error('Formato de histórico inválido');
        }

        measurementsCache = measurements.map(item => ({
            ...item,
            location: item.location ?? item.localização ?? '-',
            temperature: item.temperature ?? item.temperatura ?? null,
            humidity: item.humidity ?? item.umidade ?? null,
            air_quality: item.air_quality ?? item.qualidade_do_ar ?? null,
            measured_at: item.measured_at ?? item.medido_em ??
                item.created_at ?? ''
        }));

        if (history) {
            if (measurementsCache.length === 0) {
                history.innerHTML = `
                    <tr>
                        <td colspan="5">
                            Nenhuma medição registrada.
                        </td>
                    </tr>
                `;
            } else {
                const ordered = [...measurementsCache].sort(
                    (a, b) =>
                        new Date(b.measured_at) - new Date(a.measured_at)
                );

                history.innerHTML = ordered.map(item => {
                    const quality = classifyAirQuality(item.air_quality);

                    return `
                        <tr>
                            <td>${item.location}</td>
                            <td>${item.temperature ?? '-'} °C</td>
                            <td>${item.humidity ?? '-'} %</td>
                            <td>
                                ${item.air_quality ?? 'Não disponível'}
                                ${item.air_quality != null
                                    ? `<span style="color:${quality.color};
                                        font-weight:600">
                                        (${quality.label})
                                       </span>`
                                    : ''}
                            </td>
                            <td>${formatDate(item.measured_at)}</td>
                        </tr>
                    `;
                }).join('');
            }
        }

        renderTemperatureChart(measurementsCache);

        console.log('Histórico meteorológico:', measurementsCache);

    } catch (error) {
        console.error('Erro ao carregar histórico:', error);

        if (history) {
            history.innerHTML = `
                <tr>
                    <td colspan="5">
                        Não foi possível carregar as medições.
                    </td>
                </tr>
            `;
        }
    }
}

// BOTÕES PARA ALTERNAR OS GRÁFICOS
function setupChartButtons() {
    const buttons = document.querySelectorAll(
        '[data-indicator], [data-chart]'
    );

    buttons.forEach(button => {
        button.addEventListener('click', () => {
            const indicator =
                button.dataset.indicator ?? button.dataset.chart;

            if (!indicators[indicator]) return;

            currentIndicator = indicator;

            buttons.forEach(item => {
                item.classList.remove('active');
            });

            button.classList.add('active');

            renderTemperatureChart(measurementsCache);
        });
    });
}

// ATUALIZAÇÃO AUTOMÁTICA
const INTERVALO_ATUALIZACAO = 5 * 60 * 1000;

async function atualizarEcoPulse() {
    console.log('Atualizando indicadores do EcoPulse...');

    await Promise.all([
        loadWeather(),
        loadAirQuality(),
        loadWeatherHistory()
    ]);

    console.log('Atualização concluída!');
}

// INICIALIZAÇÃO DO SISTEMA
document.addEventListener('DOMContentLoaded', () => {
    setupChartButtons();

    atualizarEcoPulse();

    setInterval(
        atualizarEcoPulse,
        INTERVALO_ATUALIZACAO
    );
});
