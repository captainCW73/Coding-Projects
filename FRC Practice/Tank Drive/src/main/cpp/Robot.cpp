#include <frc/TimedRobot.h>
#include <frc/XboxController.h>
#include <frc/drive/DifferentialDrive.h>
#include <frc/motorcontrol/PWMSparkMax.h>
#include <frc/smartdashboard/SmartDashboard.h>  // ✅ ADD THIS

class Robot : public frc::TimedRobot {
  frc::PWMSparkMax m_leftMotor{0};
  frc::PWMSparkMax m_rightMotor{1};
  frc::DifferentialDrive m_robotDrive{
      [&](double output) { m_leftMotor.Set(output); },
      [&](double output) { m_rightMotor.Set(output); }};
  frc::XboxController m_driverController{0};

 public:
  Robot() {
    wpi::SendableRegistry::AddChild(&m_robotDrive, &m_leftMotor);
    wpi::SendableRegistry::AddChild(&m_robotDrive, &m_rightMotor);

    m_rightMotor.SetInverted(true);
  }

  void TeleopPeriodic() override {
    double left = -m_driverController.GetLeftY();
    double right = -m_driverController.GetRightY();

    // ✅ SHOW VALUES ON DASHBOARD
    frc::SmartDashboard::PutNumber("Left Y", left);
    frc::SmartDashboard::PutNumber("Right Y", right);

    m_robotDrive.TankDrive(left, right);
  }
};

#ifndef RUNNING_FRC_TESTS
int main() {
  return frc::StartRobot<Robot>();
}
#endif