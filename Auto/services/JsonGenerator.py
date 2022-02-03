"""
生成Main.json文件
For Asdb Auto tools
Version V2.0.0 - alpha
"""
import json
import time
bv = ""
templates = {
	"date": time.strftime("%m-%d", time.localtime()),
	"time": "21:30",
	"liveRoom": "A",
	"bv": bv,
	"title": "跨年夜 2021.12.31 2022好运爆棚",
	"scene": ["show"],
	"type": ["chat", "song", "dance"],
	"staff": [],
	"clip": 0,
	"items": [{
			"name": "game",
			"item": []
		}, {
			"name": "song",
			"item": [
			]
		},
		{
			"name": "dance",
			"item": [
			]
		}
	],
	"skin": {
	},
	"platform":["B","D"],
	"tags": []
}
