extends CharacterBody2D

@onready var card_scene = preload('res://other.tscn')

@onready var camera_2d: Camera2D = $Camera2D
@onready var speed = 5
var _27016 = load("res://россия.jpg")
var usa = load("res://сша.jpg")


func _process(delta: float) -> void:
	camera_2d.global_position +=  Vector2(Input.get_axis('ui_left', 'ui_right'), Input.get_axis('ui_up', 'ui_down') * speed)
	
	if Input.is_action_just_pressed('left_click'):
		pass
	elif  camera_2d.zoom > Vector2(1, 1) && Input.is_action_just_pressed('scale_down'):
		camera_2d.zoom -= Vector2(0.1, 0.1)
	elif Input.is_action_just_pressed('scale_up'):
		camera_2d.zoom += Vector2(0.1, 0.1)
	move_and_slide()



func _on_russia_pressed() -> void:
	var card_scene_ = card_scene.instantiate()
	card_scene_.open('Россия',_27016, 100000, '₽')
	add_child(card_scene_)


func _on_usa_pressed() -> void:
	var card_scene_ = card_scene.instantiate()
	
	card_scene_.open('Америка',usa, 360000, '＄')
	add_child(card_scene_)
