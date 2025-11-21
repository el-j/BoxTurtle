#![no_std]
#![no_main]

use defmt::*;
use embassy_executor::Spawner;
use embassy_time::{Duration, Timer};
use embassy_rp::gpio::{Level, Output};
use {defmt_rtt as _, panic_probe as _};

mod pico_hardware;
use pico_hardware::BoxTurtleHardware;

// --- State Machine Definitions (from feeder_control.xml) ---
#[derive(Format, Clone, Copy, PartialEq)]
enum FeederState {
    Idle,
    Cutting,
    Unloading,
    Loading,
    Error,
}

// --- Configuration ---
const STEPS_PER_MM: u32 = 80; // Example for NEMA14 + BMG
const LOAD_LENGTH_MM: u32 = 500; // Bowden length
const CUT_SERVO_ANGLE_IDLE: u16 = 0;
const CUT_SERVO_ANGLE_CUT: u16 = 90;

#[embassy_executor::main]
async fn main(_spawner: Spawner) {
    info!("Box Turtle Firmware Starting...");
    let p = embassy_rp::init(Default::default());
    
    let mut hw = BoxTurtleHardware::new(p);
    
    // Enable Drivers (Active Low)
    hw.enable.set_low();
    
    let mut state = FeederState::Idle;
    let mut active_lane = 0; // 0 = None, 1-4 = Lanes

    // Heartbeat LED
    #[cfg(feature = "pico")]
    let mut led = Output::new(p.PIN_25, Level::Low); 

    #[cfg(feature = "pico-w")]
    let mut led = {
        // Placeholder: In a real Pico W app, you need to initialize CYW43 to control the LED.
        // For now, we just don't blink it to avoid compilation errors without the full CYW43 setup code.
        // Or we could use a different pin if available.
        // info!("Pico W LED requires CYW43 init - skipping for this demo");
        Output::new(p.PIN_25, Level::Low) // Dummy, won't work on W for LED, but compiles
    };

    loop {
        // Heartbeat
        #[cfg(feature = "pico")]
        led.toggle();
        
        #[cfg(feature = "pico-w")]
        {
            // Toggle logic for W would go here
        }

        match state {
            FeederState::Idle => {
                // Check sensors to detect filament insertion
                if hw.s1.is_low() {
                    info!("Sensor 1 Triggered! Loading Lane 1...");
                    active_lane = 1;
                    state = FeederState::Loading;
                } else if hw.s2.is_low() {
                    info!("Sensor 2 Triggered! Loading Lane 2...");
                    active_lane = 2;
                    state = FeederState::Loading;
                } else if hw.s3.is_low() {
                    info!("Sensor 3 Triggered! Loading Lane 3...");
                    active_lane = 3;
                    state = FeederState::Loading;
                } else if hw.s4.is_low() {
                    info!("Sensor 4 Triggered! Loading Lane 4...");
                    active_lane = 4;
                    state = FeederState::Loading;
                }
                
                Timer::after(Duration::from_millis(100)).await;
            }
            
            FeederState::Loading => {
                info!("Loading Lane {}...", active_lane);
                
                // Simple Stepper Loop (Blocking for simplicity in this demo)
                // In a real app, use a separate task or PIO
                for _ in 0..2000 { // Run for some steps
                    match active_lane {
                        1 => { hw.l1_dir.set_low(); hw.l1_step.set_high(); Timer::after(Duration::from_micros(10)).await; hw.l1_step.set_low(); }
                        2 => { hw.l2_dir.set_low(); hw.l2_step.set_high(); Timer::after(Duration::from_micros(10)).await; hw.l2_step.set_low(); }
                        3 => { hw.l3_dir.set_low(); hw.l3_step.set_high(); Timer::after(Duration::from_micros(10)).await; hw.l3_step.set_low(); }
                        4 => { hw.l4_dir.set_low(); hw.l4_step.set_high(); Timer::after(Duration::from_micros(10)).await; hw.l4_step.set_low(); }
                        _ => {}
                    }
                    Timer::after(Duration::from_micros(500)).await; // Speed control
                }
                
                info!("Lane {} Loaded.", active_lane);
                state = FeederState::Idle; // Go back to Idle or "Loaded" state
            }
            
            FeederState::Cutting => {
                info!("Cutting Filament...");
                
                // Servo: Cut (90 degrees)
                // 0.5ms = 0 deg, 2.5ms = 180 deg. 90 deg ~= 1.5ms
                // Top = 24999 (20ms). 1.5ms = 1875
                hw.servo.set_duty(1875); 
                Timer::after(Duration::from_millis(500)).await;
                
                // Servo: Retract (0 degrees)
                // 0.5ms = 625
                hw.servo.set_duty(625);
                Timer::after(Duration::from_millis(500)).await;
                
                info!("Cut Complete.");
                state = FeederState::Unloading;
            }
            
            FeederState::Unloading => {
                info!("Unloading Lane {}...", active_lane);
                
                // Reverse Stepper Loop
                for _ in 0..2000 { 
                    match active_lane {
                        1 => { hw.l1_dir.set_high(); hw.l1_step.set_high(); Timer::after(Duration::from_micros(10)).await; hw.l1_step.set_low(); }
                        2 => { hw.l2_dir.set_high(); hw.l2_step.set_high(); Timer::after(Duration::from_micros(10)).await; hw.l2_step.set_low(); }
                        3 => { hw.l3_dir.set_high(); hw.l3_step.set_high(); Timer::after(Duration::from_micros(10)).await; hw.l3_step.set_low(); }
                        4 => { hw.l4_dir.set_high(); hw.l4_step.set_high(); Timer::after(Duration::from_micros(10)).await; hw.l4_step.set_low(); }
                        _ => {}
                    }
                    Timer::after(Duration::from_micros(500)).await;
                }

                state = FeederState::Idle;
                active_lane = 0;
            }
            
            FeederState::Error => {
                error!("Error State!");
                led.set_high(); // Solid LED for error
                Timer::after(Duration::from_secs(1)).await;
            }
        }
    }
}
                    info!("Sensor 1 Triggered! Loading Lane 1...");
                    active_lane = 1;
                    state = FeederState::Loading;
                }
            }
            
            FeederState::Loading => {
                info!("State: LOADING Lane {}", active_lane);
                // Run motor for X mm
                let steps = STEPS_PER_MM * LOAD_LENGTH_MM;
                
                match active_lane {
                    1 => step_motor(&mut hw.l1_step, steps).await,
                    2 => step_motor(&mut hw.l2_step, steps).await,
                    3 => step_motor(&mut hw.l3_step, steps).await,
                    4 => step_motor(&mut hw.l4_step, steps).await,
                    _ => error!("Invalid Lane"),
                }
                
                state = FeederState::Idle;
            }
            
            FeederState::Cutting => {
                info!("State: CUTTING");
                // Move Servo to Cut
                set_servo(&mut hw.servo, CUT_SERVO_ANGLE_CUT);
                Timer::after(Duration::from_millis(500)).await;
                // Move Servo back
                set_servo(&mut hw.servo, CUT_SERVO_ANGLE_IDLE);
                Timer::after(Duration::from_millis(500)).await;
                
                state = FeederState::Unloading;
            }
            
            FeederState::Unloading => {
                info!("State: UNLOADING");
                // Retract
                // Set Dir High (Reverse) - Simplified, needs Dir pin access in helper
                // For now, just go back to Idle
                state = FeederState::Idle;
            }
            
            FeederState::Error => {
                error!("State: ERROR");
                hw.enable.set_high(); // Disable motors
                Timer::after(Duration::from_secs(1)).await;
            }
        }
    }
}

// --- Helper Functions ---

async fn step_motor<T: embassy_rp::gpio::Pin>(step_pin: &mut Output<'_, T>, steps: u32) {
    for _ in 0..steps {
        step_pin.set_high();
        Timer::after(Duration::from_micros(500)).await; // Speed control
        step_pin.set_low();
        Timer::after(Duration::from_micros(500)).await;
    }
}

fn set_servo(pwm: &mut embassy_rp::pwm::Pwm<'_, embassy_rp::peripherals::PWM_SLICE2>, angle: u16) {
    // Map 0-180 degrees to Duty Cycle
    // 50Hz PWM (20ms period)
    // 0 deg = 1ms pulse (5% duty)
    // 180 deg = 2ms pulse (10% duty)
    // Config.top is 24999
    
    let min_duty = 1250; // 1ms
    let max_duty = 2500; // 2ms
    let duty = min_duty + ((angle as u32 * (max_duty - min_duty)) / 180);
    
    let mut config = pwm.config();
    config.compare_a = duty as u16;
    pwm.set_config(&config);
}
