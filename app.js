const ExcelJS = require('exceljs');
const { jsPDF } = require('jspdf');
const blobStream = require('blob-stream');

let svgTemplate = "";
let excelData = [];

// Fetch SVG template
async function fetchSVG() {
    try {
        const response = await fetch("./design.svg");
        if (!response.ok) throw new Error('Network response was not ok');
        svgTemplate = await response.text();
        updateSVGPreview([]);
    } catch (error) {
        console.error('Fetch error:', error);
    }
}

// Update SVG previews on the page
function updateSVGPreview(svgs = []) {
    const previewContainer = document.getElementById('svg-preview');
    previewContainer.innerHTML = '';
    svgs.forEach(svg => {
        const svgContainer = document.createElement('div');
        svgContainer.innerHTML = svg;
        previewContainer.appendChild(svgContainer);
    });
}

// Handle file upload
async function handleFile(event) {
    const file = event.target.files[0];
    const workbook = new ExcelJS.Workbook();
    const reader = new FileReader();

    reader.onload = async function(e) {
        const arrayBuffer = e.target.result;
        await workbook.xlsx.load(arrayBuffer);
        const worksheet = workbook.worksheets[0];
        const jsonData = worksheet.getSheetValues().slice(1); // Skip header

        excelData = jsonData;

        const svgList = jsonData.map(row => modifySVG(svgTemplate, row));
        updateSVGPreview(svgList);
    };

    reader.readAsArrayBuffer(file);
}

// Modify SVG with row data
function modifySVG(svg, row) {
    for (let i = 0; i < 8; i++) {
        svg = svg.replace(`{{row[${i}]}}`, row[i] || '');
    }
    return svg;
}

// Generate and download PDF
function generatePDF() {
    const doc = new jsPDF();

    // Example SVG path data
    const svgPathData = [
        { d: 'M 100 100 L 200 100 L 200 200 L 100 200 Z', fill: '#FF3300' },
        { d: 'M 300 100 L 400 100 L 400 200 L 300 200 Z', fill: '#00FF00' }
    ];

    svgPathData.forEach(pathData => {
        doc.setFillColor(pathData.fill);
        doc.path(pathData.d).fill();
    });

    doc.save('document.pdf');
}

// Attach functions to the global window object
window.generatePDF = generatePDF;
window.setup = setup;

// Set up event listeners and fetch SVG template
function setup() {
    document.getElementById('upload').addEventListener('change', handleFile, false);
    fetchSVG();
}

// Initialize
setup();
