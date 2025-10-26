@echo off
REM ========================================
REM Claude Skills Builder and Packager
REM ========================================

setlocal enabledelayedexpansion

echo.
echo ========================================
echo Claude Skills Builder
echo ========================================
echo.

REM Check if skills_config.yaml exists
if not exist "skills_config.yaml" (
    echo Error: skills_config.yaml not found!
    echo Please create your configuration file first.
    pause
    exit /b 1
)

echo [1/2] Generating prompt from configuration...
python generate_skills.py
if errorlevel 1 (
    echo.
    echo Error generating prompt!
    pause
    exit /b 1
)

echo.
echo ========================================
echo Prompt Generated Successfully!
echo ========================================
echo.
echo Location: ..\generated_skills\SKILLS_GENERATION_PROMPT.md
echo.
echo NEXT STEPS:
echo 1. Copy the generated prompt
echo 2. Paste it into Claude.ai
echo 3. Let Claude generate the skill folders
echo 4. Run this script again to package the skills
echo.
pause

echo.
echo [2/2] Packaging generated skills...
echo.

set SKILL_COUNT=0
set OUTPUT_DIR=C:\Users\Jonathan Quezada\OneDrive - Phenom People, Inc\Desktop\Claude Skills

for /d %%D in ("..\generated_skills\*") do (
    if exist "%%D\SKILL.md" (
        echo.
        echo Packaging: %%~nxD
        python package_skill.py "%%D" --no-validate --output "%OUTPUT_DIR%\%%~nxD.zip"
        
        REM Check if file was created (ignore Unicode errors)
        if exist "%OUTPUT_DIR%\%%~nxD.zip" (
            echo Created: %OUTPUT_DIR%\%%~nxD.zip
            set /a SKILL_COUNT+=1
        )
    )
)

echo.
echo ========================================
echo Packaging Complete!
echo ========================================
echo.
echo Skills packaged: %SKILL_COUNT%
echo Output location: %OUTPUT_DIR%
echo.
echo ZIP files are ready to import into Claude.ai!
echo.
pause

