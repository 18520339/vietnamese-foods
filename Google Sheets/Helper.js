function extractName(url) {
    return url.split('/').pop().split('?')[0].split('#')[0];
}

function myMsgBox(title) {
    return Browser.msgBox(
        title,
        `1. Cho tất cả các sheet (Yes)\\n
         2. Cho sheet này (No)`,
        Browser.Buttons.YES_NO
    );
}

function getSheetNames() {
    const spreadSheet = SpreadsheetApp.getActiveSpreadsheet();
    const sheetNames = spreadSheet.getSheets().map(sheet => sheet.getName());
    return sheetNames;
}

function getActiveAddress() {
    const activeSheet = SpreadsheetApp.getActiveSheet();
    const activeCell = activeSheet.getActiveCell();
    return [activeSheet, activeCell.getRow(), activeCell.getColumn()];
}

function getLastRowByCol(sheet, col) {
    const lastRow = sheet.getLastRow();
    const range = sheet.getRange(lastRow, col);
    if (range.getValue() !== '') return lastRow;
    return range.getNextDataCell(SpreadsheetApp.Direction.UP).getRow();
}

function getCurrentInfo() {
    const [activeSheet, activeRow, activeCol] = getActiveAddress();
    if (activeSheet.getName() === 'Thống kê') return;
    else if (activeRow - 1 === 0 || activeCol > 4) activeRow = 2;
    return [
        activeSheet.getName(),
        ...activeSheet.getRange(activeRow, 2, 1, 3).getValues()[0],
    ];
}

function deleteImage() {
    const [activeSheet, activeRow, activeCol] = getActiveAddress();
    if (activeSheet.getName() === 'Thống kê') return;
    activeSheet.deleteRow(activeRow);
}

function runOnActiveSheet(func, params) {
    const activeSheet = SpreadsheetApp.getActiveSheet();
    return func(activeSheet, ...params);
}

function runOnAllSheets(func, params) {
    const spreadSheet = SpreadsheetApp.getActiveSpreadsheet();
    spreadSheet.getSheets().forEach(sheet => func(sheet, ...params));
}
