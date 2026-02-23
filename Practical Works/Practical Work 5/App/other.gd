extends CanvasLayer

var boom = preload("res://animated_sprite_2d.tscn")
@onready var node_2d: Node2D = $Node2D

func open(title: String, texture: Texture2D, value: int, valut:String) -> void:
	%Label.text = title
	%Sprite2D.texture = texture 
	%Label3.text = str(value)
	%Label5.text = valut
	visible = true


func _on_button_pressed() -> void:
	$Timer.start()
	node_2d.visible = false

func _on_timer_timeout() -> void:
	var boom_ = boom.instantiate()
	
	if %Label.text == 'Россия':
		var pos = Vector2(732, 92)
		boom_.global_position = pos
		
		add_child(boom_)
	elif %Label.text == 'Америка':
		var pos = Vector2(168, 200)
		boom_.global_position = pos
		
		add_child(boom_)
		
		
		
	
