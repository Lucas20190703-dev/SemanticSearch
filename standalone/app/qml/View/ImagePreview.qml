import QtQuick
import QtMultimedia


import KQuick.Core
import KQuick.Controls

Item {
	id: _root

	property string source: ""

	property var sourceType: "image"

    property bool borderVisible: true

	readonly property size imageSize: Qt.size(_image.implicitWidth, _image.implicitHeight)
	readonly property size videoSize: Qt.size(_video.width, _video.height)
	
	readonly property bool isVideo: sourceType === "video"

	implicitWidth: isVideo? videoSize.width : imageSize.width
	implicitHeight: isVideo? videoSize.height : imageSize.height

	MediaPlayer {
        id: _player
		source: _root.isVideo? _root.source : ""
		videoOutput: _video
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
			width: 1
			color: Colors.control.border.primary
		}
	}
}