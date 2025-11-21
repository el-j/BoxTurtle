use embassy_rp::gpio::{Input, Output, Level, Pull};
use embassy_rp::pwm::{Pwm, Config as PwmConfig};
use embassy_rp::i2c::{I2c, Config as I2cConfig};
use embassy_rp::peripherals::{
    PIN_0, PIN_1, PIN_2, PIN_3, PIN_4, PIN_5, PIN_6, PIN_7, PIN_8, PIN_9, PIN_10, PIN_11, PIN_12, 
    PIN_14, PIN_15, PIN_16, PIN_17, PIN_18, PIN_19, PIN_20, PIN_21, PIN_22, 
    PWM_SLICE2, I2C1
};

// --- Hardware Configuration (Shield v2/v3) ---

// Stepper Motors (Step/Dir)
// Lane 1
pub type PinL1Step = PIN_2;
pub type PinL1Dir = PIN_3;
pub type PinL1Uart = PIN_0;

// Lane 2
pub type PinL2Step = PIN_4;
pub type PinL2Dir = PIN_5;
pub type PinL2Uart = PIN_1;

// Lane 3
pub type PinL3Step = PIN_6;
pub type PinL3Dir = PIN_7;
pub type PinL3Uart = PIN_8;

// Lane 4
pub type PinL4Step = PIN_10;
pub type PinL4Dir = PIN_11;
pub type PinL4Uart = PIN_9;

// Shared Enable
pub type PinEnable = PIN_12;

// Sensors (Input PullUp)
pub type PinSens1 = PIN_16;
pub type PinSens2 = PIN_17;
pub type PinSens3 = PIN_18;
pub type PinSens4 = PIN_19;

// Servo (PWM)
pub type PinServo = PIN_20;
pub type PwmSliceServo = PWM_SLICE2; // GP20 is on Slice 2 Channel A

// Expansion
pub type PinI2cSda = PIN_14;
pub type PinI2cScl = PIN_15;
pub type PinAux1 = PIN_21;
pub type PinAux2 = PIN_22;

// Struct to hold all hardware resources
pub struct BoxTurtleHardware {
    // Lane 1
    pub l1_step: Output<'static, PinL1Step>,
    pub l1_dir: Output<'static, PinL1Dir>,
    
    // Lane 2
    pub l2_step: Output<'static, PinL2Step>,
    pub l2_dir: Output<'static, PinL2Dir>,

    // Lane 3
    pub l3_step: Output<'static, PinL3Step>,
    pub l3_dir: Output<'static, PinL3Dir>,

    // Lane 4
    pub l4_step: Output<'static, PinL4Step>,
    pub l4_dir: Output<'static, PinL4Dir>,

    // Shared
    pub enable: Output<'static, PinEnable>,

    // Sensors
    pub s1: Input<'static, PinSens1>,
    pub s2: Input<'static, PinSens2>,
    pub s3: Input<'static, PinSens3>,
    pub s4: Input<'static, PinSens4>,

    // Servo
    pub servo: Pwm<'static, PwmSliceServo>,

    // Expansion
    pub i2c: I2c<'static, I2C1, embassy_rp::i2c::Async>,
    pub aux1: Output<'static, PinAux1>, // Default to Output, can be changed
    pub aux2: Output<'static, PinAux2>,
}

impl BoxTurtleHardware {
    pub fn new(p: embassy_rp::Peripherals) -> Self {
        // Configure Servo PWM
        let mut pwm_config = PwmConfig::default();
        pwm_config.top = 24999; // 50Hz for Servo (assuming 125MHz clock / 100 divider)
        pwm_config.divider = 100.into();
        
        let servo = Pwm::new_output_a(p.PWM_SLICE2, p.PIN_20, pwm_config.clone());

        // Configure I2C
        let i2c = I2c::new_async(p.I2C1, p.PIN_14, p.PIN_15, I2cConfig::default());

        Self {
            l1_step: Output::new(p.PIN_2, Level::Low),
            l1_dir: Output::new(p.PIN_3, Level::Low),
            
            l2_step: Output::new(p.PIN_4, Level::Low),
            l2_dir: Output::new(p.PIN_5, Level::Low),
            
            l3_step: Output::new(p.PIN_6, Level::Low),
            l3_dir: Output::new(p.PIN_7, Level::Low),
            
            l4_step: Output::new(p.PIN_10, Level::Low),
            l4_dir: Output::new(p.PIN_11, Level::Low),
            
            enable: Output::new(p.PIN_12, Level::High), // Active Low usually, but start High (Disabled)
            
            s1: Input::new(p.PIN_16, Pull::Up),
            s2: Input::new(p.PIN_17, Pull::Up),
            s3: Input::new(p.PIN_18, Pull::Up),
            s4: Input::new(p.PIN_19, Pull::Up),
            
            servo,

            i2c,
            aux1: Output::new(p.PIN_21, Level::Low),
            aux2: Output::new(p.PIN_22, Level::Low),
        }
    }
}
        }
    }
}
