#!/bin/bash
# Homebrew formula for Smart Attendance System
# Save this as: smart-attendance.rb in your homebrew-core fork

class SmartAttendance < Formula
  desc "Face Recognition Attendance Management System with Beautiful TUI"
  homepage "https://github.com/yourusername/smart-attendance"
  url "https://github.com/yourusername/smart-attendance/archive/v1.0.0.tar.gz"
  sha256 "REPLACE_WITH_ACTUAL_SHA256"
  license "MIT"

  depends_on "python@3.11"
  depends_on "cmake"
  depends_on "opencv"

  def install
    virtualenv_install_with_resources
    bin.install_symlink libexec/"bin/smart-attendance"
  end

  test do
    system "#{bin}/smart-attendance", "--help"
  end
end
