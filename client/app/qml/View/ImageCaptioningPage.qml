import QtQuick 2.15
import QtQuick.Controls 2.15

import KQuick.Core 1.0
import KQuick.Controls 1.0
import Utils 1.0

BasePage {
	id: _root
	title: qsTr("Image Captioning")

	QtObject {
		id: d
		property bool imageSourceChanged: false
	}

	SplitView {
		id: _hSplitView
		anchors.fill: parent
		
		handle: KSplitHandle {}
		clip: true

		FileListView {
			id: _sourceLIstView
			SplitView.fillHeight: true
			SplitView.preferredWidth: 200
			SplitView.minimumWidth: 160
		}

		Item {
			SplitView.fillHeight: true
			SplitView.fillWidth: true

			SplitView {
				id: _vSplitView
				anchors.fill: parent
				orientation: Qt.Vertical

				handle: KSplitHandle { }

				ImagePreview {
					id: _imagePreview
					SplitView.fillWidth: true
					SplitView.fillHeight: true
					source: _sourceLIstView.currentImage

					onSourceChanged: {
						_root.getCaption(source);
					}
				}

				CaptionView {
					id: _captionView
					SplitView.fillWidth: true
					SplitView.preferredHeight: 150
					SplitView.minimumHeight: 80
					SplitView.maximumHeight: 200
				}
			}
		}
	}

	function getCaption(imageSource) {
		imageSource = Constants.removePrefix(imageSource)
		if (!imageSource || imageSource.length < 1)
		{
			return;
		}
		_captionView.busy = true;
		_captionView.caption = "";
		
		var xhr = new XMLHttpRequest();
		xhr.open("GET", Constants.apiCaption + encodeURIComponent(imageSource));
		//xhr.setRequestHeader("Authorization", "Bearer YOUR_TOKEN_HERE");
		xhr.onreadystatechange = function() {
			if (xhr.readyState === XMLHttpRequest.DONE) {
				if (xhr.status === 200) {
					var data = JSON.parse(xhr.responseText);
					console.log("Response:", JSON.stringify(data));
					// Use data.caption here
					_captionView.caption = data.caption;
					_captionView.busy = false;
				} else {
					console.log("Error:", xhr.status, xhr.responseText);
				}
			}
		}
		xhr.send();
	}
}