import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import KQuick.Controls
import KQuick.Core
import Utils

BasePage {
    id: _root
    title: qsTr("Search")
    
    property var selected: null

    ColumnLayout {
        anchors.fill: parent
        SearchPanel {
            id: _searchPanel
            Layout.fillWidth: true
            
            onSearchClicked: (params) => {
                postSearchRequest(params)
            }
        }
        
        KSeparator {
            Layout.fillWidth: true
        }

        Flickable {
            Layout.fillWidth: true
            Layout.fillHeight: true

            contentWidth: width
            contentHeight: grid.height
            clip: true

            flickableDirection: Flickable.AutoFlickIfNeeded

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
                        required property var name
                        required property var path
                        required property var caption
                        required property var filePath // including api

                        readonly property var fileType: fileHelper.isVideo(path) || "Unknown"

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
                                onTapped: _root.selected = { fileName: name, filePath, fileType }
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
                            text: name
                            font.pointSize: 8
                            elide: Text.ElideRight
                        }
                    }
                }
            }

            ScrollBar.vertical: ScrollBar {}
        }
    }

    ListModel { id: _mediaModel }


    function postSearchRequest(bodyObj, callback) {
        var xhr = new XMLHttpRequest();
        xhr.open("POST", Constants.apiSearch);
        xhr.setRequestHeader("Content-Type", "application/json");

        xhr.onreadystatechange = function() {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                if (xhr.status === 200) {
                    var files = JSON.parse(xhr.responseText);
                    _mediaModel.clear();
                    for (let i = 0; i < files.length; ++i) {
                        let file = files[i];
                        file['filePath'] = `${Constants.apiMedia}${file['path']}`;
                        _mediaModel.append(file);
                    }

                    if (callback) {
                        callback(json); // return results to QML UI
                    }

                } else {
                    console.log("Search failed:", xhr.status, xhr.responseText);
                }
            }
        }

        xhr.send(JSON.stringify(bodyObj));
    }
}