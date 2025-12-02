import QtQuick 2.15
import QtQuick.Controls 2.15

import KQuick.Controls 1.0
import KQuick.Core 1.0

Pane {
	id: _root

	property alias caption : _caption.text

	property alias busy: _indicator.running

	background: KRectangle { }

	padding: 16
	topPadding: 10

	TextInput {
		id: _caption
		width: parent.width
		wrapMode: Text.Wrap
		readOnly: true
		selectByMouse: true
		color: Colors.foreground.primary
		font.pointSize: 11		
	}

	KLoadIndicator {
		id: _indicator
		anchors.centerIn: parent
		color: Colors.control.foreground.primary
		useDouble: true
		radius: 16
		running: false
		visible: running
	}
}