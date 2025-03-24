// Main JavaScript for Real Estate Valuation and Negotiation Strategist

// Format number with commas
function formatNumber(num) {
    return new Intl.NumberFormat().format(Math.round(num));
}

// Capitalize first letter of a string
function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

// Format currency
function formatCurrency(num) {
    return '$' + formatNumber(num);
}

// Format percentage
function formatPercentage(num, decimals = 1) {
    return num.toFixed(decimals) + '%';
}

// Calculate price difference percentage
function calculatePriceDiff(listingPrice, estimatedValue) {
    if (listingPrice > 0 && estimatedValue > 0) {
        return ((listingPrice - estimatedValue) / estimatedValue * 100).toFixed(1);
    }
    return 0;
}

// Get price difference class
function getPriceDiffClass(priceDiff) {
    if (priceDiff > 5) {
        return 'text-danger';
    } else if (priceDiff < -5) {
        return 'text-success';
    } else {
        return 'text-muted';
    }
}

// Get price difference text
function getPriceDiffText(priceDiff) {
    if (priceDiff > 5) {
        return `Overpriced by ${priceDiff}%`;
    } else if (priceDiff < -5) {
        return `Underpriced by ${Math.abs(priceDiff)}%`;
    } else {
        return `Fair price (±${Math.abs(priceDiff)}%)`;
    }
}

// Get motivation class
function getMotivationClass(level) {
    if (level === 'high') {
        return 'text-success';
    } else if (level === 'moderate') {
        return 'text-warning';
    } else {
        return 'text-danger';
    }
}

// Add table row with label and value
function addTableRow(table, label, value) {
    const row = table.insertRow();
    const labelCell = row.insertCell(0);
    const valueCell = row.insertCell(1);
    labelCell.innerHTML = `<strong>${label}</strong>`;
    valueCell.textContent = value;
    return row;
}

// Add cell to row
function addCell(row, text) {
    const cell = row.insertCell();
    cell.textContent = text;
    return cell;
}

// Create a chart
function createChart(ctx, type, labels, datasets, options = {}) {
    return new Chart(ctx, {
        type: type,
        data: {
            labels: labels,
            datasets: datasets
        },
        options: options
    });
}
