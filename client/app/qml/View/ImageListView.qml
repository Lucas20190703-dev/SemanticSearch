import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15

import KQuick.Controls 1.0
import KQuick.Core 1.0

ColumnLayout {
    property alias rootDir: _imageGrid.rootDir

    readonly property alias selectedItem: _imageGrid.selected
    
    spacing: 0
    
    SearchPanel {
        id: _searchPanel
        Layout.fillWidth: true
        
        onNameFilterChanged: {
            //searchEngine.fileModel.setSearchText(nameFilter);
        }

        onCaptionFilterChanged: {
            //searchEngine.fileModel.setSearchCaption(captionFilter);
        }

        onSimilarityChanged: {
            //searchEngine.fileModel.setSearchCaptionThreshold(similarity);
        }

        onStartDateFilterChanged: {
            //searchEngine.fileModel.setSearchDate(startDateFilter, endDateFilter);
        }

        onEndDateFilterChanged: {
            //searchEngine.fileModel.setSearchDate(startDateFilter, endDateFilter);
        }
    }
    
    KSeparator {
        Layout.fillWidth: true
    }

    ImageSearchContentView {
        id: _imageGrid
        Layout.fillWidth: true
        Layout.fillHeight: true
    }
}
