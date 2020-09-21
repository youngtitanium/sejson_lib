>>>from sejson import sejson

>>>file = sejson('SomeJSON.json')

>>>file.update("settings", {"delay":10, "creator_ids": [1, 2, 3]})
True
>>>beauty = file.beauty(False)

>>>print(beauty)
{
	"settings": {
		"delay": 10,
		"creator_ids": [
			1,
			2,
			3
		]
	}
}
>>>file0 = sejson('SomeJSON.json')

>>>file0.append('destruct')
True
>>>print(file0.beauty(False))
[
	"destruct"
]