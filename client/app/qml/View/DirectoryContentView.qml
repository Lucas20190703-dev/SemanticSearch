import QtQuick
import QtQuick.Controls
import KQuick.Controls
import KQuick.Core
import Utils

Item {
    id: _root
    property var folder
    property int offset: 0
    property int limit: 40
    property bool loading: false
    property bool hasMore: true

    property var selected: null

    function loadMore() {
        if (!folder || loading || !hasMore)
            return;

        loading = true;
        const xhr = new XMLHttpRequest();
        xhr.open("GET", Constants.apiFiles +
                 encodeURIComponent(folder) +
                 `?offset=${offset}&limit=${limit}`);
        xhr.onreadystatechange = function () {
            if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
                const files = JSON.parse(xhr.responseText);
                if (files.length < limit)
                    hasMore = false;
                for (let i = 0; i < files.length; ++i) {
                    let file = files[i];
                    file['filePath'] = `${Constants.apiMedia}${file['filePath']}`;
                    _mediaModel.append(file);
                    console.log("File:", JSON.stringify(file))
                }
                offset += files.length;
                loading = false;
            }
        };
        xhr.send();
    }

    onFolderChanged: {
        _mediaModel.clear();
        offset = 0;
        hasMore = true;
        loadMore();
    }

    
    Rectangle {
        anchors.fill: parent
        color: Colors.background.primary
    }

    ListModel { id: _mediaModel }

    Flickable {
        anchors.fill: parent
        contentWidth: width
        contentHeight: grid.height
        clip: true

        flickableDirection: Flickable.AutoFlickIfNeeded

        onContentYChanged: {
            if ((contentY + height) >= (contentHeight - 100)) {
                loadMore();
            }
        }

        Grid {
            id: grid
            width: parent.width
            property int cellWidth: 160 + 12
            property int cellHeight: 90
            columns: Math.max(1, Math.floor(width / cellWidth))
            columnSpacing: (columns < 2) ? 6 : (width - columns * cellWidth) / (columns - 1)
            rowSpacing: 10

            anchors.margins: 16

            Repeater {
                id: _itemRepeater
                model: _mediaModel
                delegate: Column {
                    required property var fileName
                    required property var filePath
                    required property var fileType
                    required property int fileSize
                    required property int modified

                    width: grid.cellWidth
                    spacing: 4
                    
                    readonly property bool isSelected: _root.selected && _root.selected.filePath === filePath

                    MediaItem {
                        anchors.horizontalCenter: parent.horizontalCenter
                        width: grid.cellWidth - 12
                        height: grid.cellHeight
                        source: filePath
                        sourceType: fileType
                        highlight: _root.selected && _root.selected.filePath === filePath
                        TapHandler {
                            onDoubleTapped: openPreviewImage(filePath, fileType);
                            onTapped: _root.selected = { fileName, filePath, fileType, fileSize, modified }
                        }

                        KIcon {
                            anchors.centerIn: parent
                            width: 32
                            height: 32
                            visible: fileType === "video"
                            icon {
                                width: 32
                                height: 32
                                source: "qrc:/icons/video-player.png"
                                color: Colors.accent.highlight
                            }
                        }
                    }

                    KText {
                        anchors.horizontalCenter: parent.horizontalCenter
                        width: Math.min((parent.width - 12) * 0.8, implicitWidth)
                        text: fileName
                        font.pointSize: 8
                        elide: Text.ElideRight
                    }
                }
            }
        }

        ScrollBar.vertical: ScrollBar {}
    }
}
