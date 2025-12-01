import QtQuick 2.15
import QtQuick.Controls 2.15

import KQuick.Core 1.0
import KQuick.Controls 1.0

Rectangle {
    id: _root

    // property alias titlebar: _titlebar
    
    color: Colors.background.primary

    // KTitleBar {
    //     id: _titlebar
    //     width: parent.width
    //     height: 30

    //     window: mainWindow

    //     onMinimize: {
    //         mainWindow.showMinimized()
    //     }

    //     onMaximize: {
    //         if (maximizeButton.checked) {
    //             mainWindow.showNormal()
    //         }
    //         else {
    //             mainWindow.showMaximized()
    //         }
    //     }

    //     onClose: {
    //         mainWindow.close();
    //     }
    // }

    ContentView {
        anchors.fill: parent
        // anchors.topMargin: _titlebar.height
    }

    Popup {
        id: _previewPopup
        property string source
        property string sourceType

        anchors.centerIn: parent
        
        width: parent.width * 0.8
        height: parent.height * 0.8

        focus: true
        modal: true

        background: Rectangle {
            color: "transparent"
        }
        Overlay.modal: Rectangle {
            color: "#80000000"
        }

        contentItem: MediaItem {
            source: _previewPopup.source
            sourceType: _previewPopup.sourceType
            borderVisible: false
            isThumbnail: false
            onVisibleChanged: {
                if (!isVideo) {
                    return;
                }
                if (visible) {
                    play();
                }
                else {
                    pause();
                }
            }
        }
    }

    function openPreviewImage(source, fileType) {
        _previewPopup.source = source;
        _previewPopup.sourceType = fileType;
        _previewPopup.open()
    }
}