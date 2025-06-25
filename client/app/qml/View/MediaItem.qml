import QtQuick
import QtMultimedia


import KQuick.Core
import KQuick.Controls

Item {
	id: _root

	property string source: ""

	property var sourceType: "image"

    property bool highlight: false

    property bool borderVisible: true

    property bool isThumbnail: true
    
	readonly property size imageSize: Qt.size(_image.implicitWidth, _image.implicitHeight)
	readonly property size videoSize: Qt.size(_video.width, _video.height)
	
	readonly property bool isVideo: sourceType === "video"

	implicitWidth: isVideo? videoSize.width : imageSize.width
	implicitHeight: isVideo? videoSize.height : imageSize.height

    Timer {
        id: _timer
        interval: 1000
        
        onTriggered: {
            if (!_root.isThumbnail) {
                _player.stop();
                return;
            }

            if (_player.playing) {
                _player.pause() // for thumbnail, TODO: resource management
            }
        }
    }

	MediaPlayer {
        id: _player
		source: _root.isVideo? _root.source : ""
		videoOutput: _video
        Component.onCompleted: {
            if (source) {
                _player.play();
            }
            if (_root.isThumbnail) {
                _timer.start();
            }
        }
    }

	VideoOutput {
		id: _video
        anchors.fill: parent
		visible: _root.isVideo
		fillMode: Image.PreserveAspectFit
	}

	Image {
		id: _image

		anchors {
			fill: parent
			margins: 1
		}

		asynchronous: true
		visible: !_root.isVideo
		source: !_root.isVideo? _root.source : ""
		sourceSize: Qt.size(parent.width, parent.height)
		fillMode: Image.PreserveAspectFit
	}

	Rectangle {
		anchors.fill: parent
		color: "transparent"
		visible: _root.borderVisible

		border {
			width: _root.highlight? 2 : 1
			color: _root.highlight? Colors.control.border.highlight : Colors.control.border.primary
		}
	}

    function play() {
        if (_timer.running) {
            _timer.stop();
            _player.seek(0);
        }
        _player.play();
    }

    function pause() {
        _player.pause();
    }
}