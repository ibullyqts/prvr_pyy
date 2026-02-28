name: Phoenix V100 Mega-Matrix

on:
  workflow_dispatch:
  schedule:
    - cron: '0 */4 * * *'

jobs:
  mega-strike:
    strategy:
      matrix:
        # 🚀 This spawns 10 separate machines at the same time
        machine_id: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    runs-on: ubuntu-latest
    timeout-minutes: 350 

    steps:
    - name: Checkout Code
      uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'

    - name: Install Dependencies
      run: pip install selenium==4.21.0 selenium-stealth

    - name: 🔥 Run Machine ${{ matrix.machine_id }}
      env:
        INSTA_COOKIE: ${{ secrets.INSTA_COOKIE }}
        TARGET_THREAD_ID: ${{ secrets.TARGET_THREAD_ID }}
        MESSAGES: ${{ secrets.MESSAGES }}
        MACHINE_ID: ${{ matrix.machine_id }}
      run: |
        while true; do
          python -u main.py
          echo "⚠️ Machine ${{ matrix.machine_id }} Restarting..."
          sleep 5
        done
