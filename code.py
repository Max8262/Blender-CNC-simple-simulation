import bpy

obj_x = bpy.data.objects["Object_X"]
obj_y = bpy.data.objects["Object_Y"]
obj_z = bpy.data.objects["Object_Z"]
track = bpy.data.objects["Track"]

init_pos_x = (0, -31.223, 4.8598)
init_pos_y = (0, 0, 10.675)
init_pos_z = (3.9136, 0, 11.077)
init_pos_track = (6.5218, 0, 2.4333)

def clear_animations_and_reset():
    if obj_x.animation_data:
        obj_x.animation_data_clear()
    if obj_y.animation_data:
        obj_y.animation_data_clear()
    if obj_z.animation_data:
        obj_z.animation_data_clear()
    if track.animation_data:
        track.animation_data_clear()

    obj_x.location = init_pos_x
    obj_y.location = init_pos_y
    obj_z.location = init_pos_z
    track.location = init_pos_track

    bpy.context.scene.frame_set(0)

    obj_x.keyframe_insert(data_path="location", frame=0)
    obj_y.keyframe_insert(data_path="location", frame=0)
    obj_z.keyframe_insert(data_path="location", frame=0)
    track.keyframe_insert(data_path="location", frame=0)

    bpy.context.view_layer.update()

def move_objects_through_points(points, total_frames=100):
    start_frame = bpy.context.scene.frame_current
    num_points = len(points)
    frames_per_move = total_frames // (num_points - 1) if num_points > 1 else total_frames

    for i in range(num_points - 1):
        start_pos = points[i]
        target_pos = points[i + 1]
        start_x, start_y, start_z = start_pos
        target_x, target_y, target_z = target_pos
        end_frame = start_frame + (i + 1) * frames_per_move

        obj_x.location = (start_x - 6.5218, init_pos_x[1], init_pos_x[2])
        obj_y.location = (start_x - 6.5218, start_y, init_pos_y[2])
        obj_z.location = (start_x - 2.6082, start_y, start_z + 8.6437)
        track.location = (start_x, start_y, start_z)
        obj_x.keyframe_insert(data_path="location", frame=start_frame + i * frames_per_move)
        obj_y.keyframe_insert(data_path="location", frame=start_frame + i * frames_per_move)
        obj_z.keyframe_insert(data_path="location", frame=start_frame + i * frames_per_move)
        track.keyframe_insert(data_path="location", frame=start_frame + i * frames_per_move)

        obj_x.location = (target_x - 6.5218, init_pos_x[1], init_pos_x[2])
        obj_y.location = (target_x - 6.5218, target_y, init_pos_y[2])
        obj_z.location = (target_x - 2.6082, target_y, target_z + 8.6437)
        track.location = (target_x, target_y, target_z)
        obj_x.keyframe_insert(data_path="location", frame=end_frame)
        obj_y.keyframe_insert(data_path="location", frame=end_frame)
        obj_z.keyframe_insert(data_path="location", frame=end_frame)
        track.keyframe_insert(data_path="location", frame=end_frame)

    bpy.context.view_layer.update()

def draw_motion_paths(objects, start_frame, end_frame):
    bpy.context.scene.frame_start = start_frame
    bpy.context.scene.frame_end = end_frame
    for obj in objects:
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        bpy.ops.object.paths_calculate()
        obj.select_set(False)

def delete_motion_paths(objects):
    for obj in objects:
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        bpy.ops.object.paths_clear()
        obj.select_set(False)

delete_motion_paths([obj_x, obj_y, obj_z, track])

points = [
    (0, 0, 1),
    (10, 8, 2),
    (0, 0, 1.5),
    (20, 20, 1.23),
    (20, -10, 1)
]

total_frames = 100
move_objects_through_points(points, total_frames)

start_frame = 0
end_frame = total_frames
draw_motion_paths([track], start_frame, end_frame)
