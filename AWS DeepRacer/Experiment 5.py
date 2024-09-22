break_speed = 0.01

def reward_function(params):
    
    # Track details
    track_width = 1.7     
    track_length = 16.64 

    # input parameters
    distance_from_center = params['distance_from_center']
    all_wheels_on_track = params['all_wheels_on_track']
    speed = params['speed']
    closest_waypoints = params['closest_waypoints']
    progress = params['progress']
    steps = params['steps']
    
    # Calculate the distance from the nearest border
    distance_from_border = 0.5 * track_width - distance_from_center

    # Reward higher if the car stays inside the track borders (at least 5 cm away from the edge)
    if distance_from_border >= 0.05:
        center_line_reward = 1.0
    else:
        center_line_reward = 1e-3  # Low reward if too close to the border or off track

    # Reward based on wheels on track and speed
    SPEED_THRESHOLD = 1.0
    wp_index = closest_waypoints[1]  
    
    if not all_wheels_on_track:
        track_and_speed_reward = 1e-3
    elif speed < SPEED_THRESHOLD:
        track_and_speed_reward = 0.5
    else:
        track_and_speed_reward = 1.0

    # Adjust reward based on specific waypoints and speed
    if wp_index in range(22,40) or wp_index in range(50, 56) or wp_index in range(67, 72) or wp_index in range(80, 87) or wp_index in range(105, 112):
        if speed >= 2.5:
            track_and_speed_reward = break_speed

    # Total number of steps we want the car to finish the lap (based on track length)
    TOTAL_NUM_STEPS = 300
    
    # Initialize the reward
    reward = center_line_reward * track_and_speed_reward
    
    # Add reward for progress every 100 steps, if faster than expected
    if (steps % 100) == 0 and progress > (steps / TOTAL_NUM_STEPS) * 100:
        reward += 10.0

    return float(reward)
