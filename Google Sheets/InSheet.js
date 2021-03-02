function removeDuplicatesInSheet(currentSheet) {
    if (currentSheet.getName() === 'Thống kê') return;
    currentSheet.activate();

    const currentData = currentSheet.getDataRange().getValues();
    const newData = [];

    for (let i in currentData) {
        let url = currentData[i][1];
        let duplicate = false;

        for (let j in newData) if (url == newData[j][0]) duplicate = true;
        if (!duplicate) newData.push(currentData[i].slice(1, 3));
    }

    currentSheet
        .getRange(1, 2, currentData.length, newData[0].length)
        .clearContent();

    currentSheet
        .getRange(1, 2, newData.length, newData[0].length)
        .setValues(newData);

    return newData.length - 2;
}

function downloadUrlsInSheet(currentSheet, urlsFolder) {
    if (currentSheet.getName() === 'Thống kê') return;
    currentSheet.activate();

    const lastRow = getLastRowByCol(currentSheet, 2);
    const fileName = `${currentSheet.getName()}.txt`;
    const file = urlsFolder.getFilesByName(fileName);

    const dataRange = currentSheet.getRange(2, 2, lastRow - 1, 1);
    const fileContent = dataRange.getValues().join('\n');

    if (file.hasNext()) file.next().setContent(fileContent);
    else urlsFolder.createFile(fileName, fileContent);
    return dataRange.getNumRows();
}

function syncToDriveInSheet(currentSheet, datasetFolder, urlsFolder) {
    const sheetName = currentSheet.getName();
    if (sheetName === 'Thống kê') return 0;
    currentSheet.activate();

    const imagesFolder = datasetFolder.getFoldersByName(sheetName).next();
    const files = imagesFolder.getFiles();

    let imagesInDrive = [];
    while (files.hasNext()) imagesInDrive.push(files.next());

    const urlsFile = urlsFolder.getFilesByName(`${sheetName}.txt`).next();
    const urlsInDrive = urlsFile.getBlob().getDataAsString().split('\n');

    if (imagesInDrive.length !== urlsInDrive.length) return 0;
    imagesInDrive = imagesInDrive.sort((a, b) => {
        return a.getName().localeCompare(b.getName(), undefined, {
            numeric: true,
            sensitivity: 'base',
        });
    });

    const lastRow = getLastRowByCol(currentSheet, 2);
    const dataRange = currentSheet.getRange(2, 2, lastRow - 1, 1);
    const urlsInSheet = dataRange.getValues().flat();

    let startRename = false;
    for (let i = 0; i < urlsInSheet.length; ++i) {
        if (startRename) imagesInDrive[i].setName(`${i + 1}.jpg`);
        if (urlsInSheet[i] !== urlsInDrive[i]) {
            imagesInDrive[i].setTrashed(true);
            imagesInDrive.splice(i, 1);
            urlsInDrive.splice(i, 1);
            startRename = true;
            i -= 1;
        }
    }

    urlsFile.setContent(urlsInSheet.join('\n'));
    return imagesInDrive.length;
}

function setImageCellsSizeInSheet(currentSheet, newSize) {
    if (currentSheet.getName() === 'Thống kê') return;
    currentSheet.activate();

    const height = newSize[0] ? Number(newSize[0]) : 200;
    const width = newSize[1] ? Number(newSize[1]) : 350;

    currentSheet.setRowHeights(2, currentSheet.getLastRow() - 1, height);
    currentSheet.setColumnWidth(1, width);
}
