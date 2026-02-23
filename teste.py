#!/usr/bin/env python3

import rclpy
import time
import asyncio

from go2_robot_sdk.presentation.go2_driver_node import Go2DriverNode
from go2_robot_sdk.domain.constants import ROBOT_CMD
from go2_robot_sdk.application.utils.command_generator import gen_command, gen_mov_command

async def working_rotation():
    rclpy.init()
    
    current_loop = asyncio.get_running_loop()
    node = Go2DriverNode(event_loop=current_loop)
    
    node.get_logger().info('Connecting to robot...')
    await node.connect_robots()
    await asyncio.sleep(8.0)
    
    try:
        # 1. Stand Up
        node.get_logger().info('Standing up...')
        stand_cmd = gen_command(1004, "1004", "rt/api/sport/request")
        node.webrtc_adapter.send_command("0", stand_cmd)
        await asyncio.sleep(5.0)
        
        # 2. Balance Stand (required for movement)
        node.get_logger().info('Entering balance stand...')
        balance_cmd = gen_command(1002, "1002", "rt/api/sport/request")
        node.webrtc_adapter.send_command("0", balance_cmd)
        await asyncio.sleep(3.0)
        
        # 3. Hello
        node.get_logger().info('Saying hello...')
        hello_cmd = gen_command(ROBOT_CMD["Hello"], str(ROBOT_CMD["Hello"]), "rt/api/sport/request")
        node.webrtc_adapter.send_command("0", hello_cmd)
        await asyncio.sleep(5.0)
        
        # 4. ROTATION - Send continuous movement commands
        node.get_logger().info('Starting rotation...')
        
        # Send rotation commands continuously for 5 seconds
        start_time = time.time()
        while time.time() - start_time < 5.0:
            rotation_cmd = gen_mov_command(0.0, 0.0, 0.5)  # Higher rotation value
            node.webrtc_adapter.send_command("0", rotation_cmd)
            await asyncio.sleep(0.1)  # 10Hz
            
        # 5. Stop
        node.get_logger().info('Stopping...')
        stop_cmd = gen_mov_command(0.0, 0.0, 0.0)
        node.webrtc_adapter.send_command("0", stop_cmd)
        
        node.get_logger().info('Rotation test complete!')
        
    except Exception as e:
        node.get_logger().error(f'Error: {e}')
    finally:
        node.destroy_node()
        rclpy.shutdown()

def main():
    asyncio.run(working_rotation())

if __name__ == '__main__':
    main()