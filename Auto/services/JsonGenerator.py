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
	"staff": ["A", "B", "C", "D", "E"],
	"clip": 3,
	"items": [{
			"name": "game",
			"item": []
		}, {
			"name": "song",
			"item": [
				["哈喽 哈喽", "1-18:52", ["A"]],
				["桃花朵朵开", "1-34:51", ["C"]],
				["桃花笑", "1-50:13", ["E"]],
				["蜀绣", "2-20:05", ["E"]],
				["人间惊鸿客", "2-39:12", ["B"]],
				["小年兽", "2-54:18", ["D"]],
				["小永远", "3-00:24", ["E"]],
				["小幸运", "3-29:57", ["A", "B", "C", "D", "E"]]
			]
		},
		{
			"name": "dance",
			"item": [
				["BOOM", "1-09:55", ["A", "B", "C", "D", "E"]],
				["Uptown Funk", "1-25:55", ["B"]],
				["醉太平", "1-43:47", ["D"]],
				["Bingle Bangle", "1-64:14", ["A"]],
				["美人关", "2-02:16", ["B"]],
				["情人", "2-07:44", ["C"]],
				["花月成双", "2-14:10", ["D"]],
				["Dun Dun Dance", "2-32:34", ["A"]],
				["自作多情", "2-47:55", ["C"]]
			]
		}
	],
	"skin": {
		"A": ["official", "christmas", "swim", "group", "year"],
		"B": ["official", "group", "LegendWorld", "year", "swim", "birthday"],
		"C": ["official", "birthday", "LegendWorld", "swim", "group", "year"],
		"D": ["official", "LegendWorld", "year", "group", "swim", "chinese"],
		"E": ["official", "LegendWorld", "group", "year", "swim", "birthday"]
	},
	"platform": "B",
	"tags": []
}

