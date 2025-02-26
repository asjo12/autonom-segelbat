class PIDController:
    def __init__(self, Kp = 1.0, Ki = 0.01, Kd= 0.01):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.prev_error = 0
        self.integral = 0

    def update(self, setpoint, process_variable, dt = 0.1):
        error = setpoint - process_variable

        # Proportional term
        P = self.Kp * error

        # Integral term
        self.integral += error * dt
        I = self.Ki * self.integral

        # Derivative term
        derivative = (error - self.prev_error) / dt
        D = self.Kd * derivative

        # PID output
        output = P + I + D

        # Save the current error for the next iteration
        self.prev_error = error

        return output

"""
# Example usage
if __name__ == "_main_":
    # Set the PID parameters and initial conditions
    Kp = 1.0
    Ki = 0.1
    Kd = 0.01

    # Reference value (setpoint)
    setpoint = 20.0

    # Initial condition for the process variable
    process_variable = 15.0

    # Create a PID controller
    pid_controller = PIDController(Kp, Ki, Kd)

    # Simulation loop
    time_step = 0.1
    total_time = 10.0
    steps = int(total_time / time_step)

    for _ in range(steps):
        # Update the PID controller and get the control output
        control_output = pid_controller.update(setpoint, process_variable, time_step)

        # Simulate a system response (e.g., a process or plant)
        # For simplicity, we'll assume a first-order system
        # with a time constant of 1.0
        system_time_constant = 1.0
        process_variable += (control_output - process_variable) * (time_step / system_time_constant)

        print(f"Time: {_ * time_step:.2f}, Process Variable: {process_variable:.2f}, Control Output: {control_output:.2f}")"""