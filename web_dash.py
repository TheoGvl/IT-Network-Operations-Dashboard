from nicegui import ui
import psutil
from datetime import datetime
import platform

# Enable Dark Mode for a professional IT look
ui.dark_mode().enable()

# Initialize lists for the chart (storing the last 20 measurements)
cpu_history = []
time_history = []

# --- Header ---
with ui.header(elevated=True).classes('bg-slate-900 items-center px-6 py-3'):
    ui.icon('monitor_heart', size='md').classes('text-emerald-400')
    ui.label('System & Network Operations').classes('text-2xl font-bold ml-3 text-white')
    ui.space()
    clock_label = ui.label().classes('text-gray-300 font-mono text-lg')

# --- Main Layout ---
with ui.column().classes('w-full max-w-6xl mx-auto p-6 gap-6'):
    
    # 1. System Info Banner
    with ui.row().classes('w-full items-center justify-between bg-slate-800 p-4 rounded-lg shadow-lg'):
        ui.label(f'Host: {platform.node()}').classes('text-emerald-400 font-bold text-lg')
        ui.label(f'OS: {platform.system()} {platform.release()}').classes('text-gray-300')
        ui.label(f'Processor: {platform.processor()}').classes('text-gray-300 text-sm')

    # 2. Key Metrics Cards (CPU, RAM, Network)
    with ui.row().classes('w-full justify-between gap-4'):
        
        # CPU Card
        with ui.card().classes('flex-1 bg-slate-800 text-center items-center shadow-lg'):
            ui.label('CPU Usage').classes('text-gray-400 font-semibold')
            cpu_ring = ui.circular_progress(min=0, max=100, show_value=True).props('size=80px color=emerald font-size=20px thickness=0.2')
            
        # RAM Card
        with ui.card().classes('flex-1 bg-slate-800 text-center items-center shadow-lg'):
            ui.label('Memory (RAM)').classes('text-gray-400 font-semibold')
            ram_ring = ui.circular_progress(min=0, max=100, show_value=True).props('size=80px color=blue font-size=20px thickness=0.2')
            ram_text = ui.label('0 GB / 0 GB').classes('text-xs mt-2 text-gray-400')

        # Network Traffic Card
        with ui.card().classes('flex-1 bg-slate-800 items-center shadow-lg'):
            ui.label('Network Traffic (Bytes)').classes('text-gray-400 font-semibold mb-2')
            with ui.row().classes('w-full justify-around mt-2'):
                with ui.column().classes('items-center'):
                    ui.icon('arrow_downward', color='green').classes('text-2xl')
                    net_recv_label = ui.label('0 B').classes('font-mono text-sm text-gray-300')
                with ui.column().classes('items-center'):
                    ui.icon('arrow_upward', color='orange').classes('text-2xl')
                    net_sent_label = ui.label('0 B').classes('font-mono text-sm text-gray-300')

    # 3. Live CPU Chart
    with ui.card().classes('w-full bg-slate-800 shadow-lg mt-2'):
        ui.label('CPU Performance History').classes('text-gray-400 font-semibold mb-2')
        cpu_chart = ui.echart({
            'xAxis': {'type': 'category', 'data': [], 'axisLine': {'lineStyle': {'color': '#9ca3af'}}},
            'yAxis': {'type': 'value', 'max': 100, 'splitLine': {'lineStyle': {'color': '#374151'}}},
            'series': [{'type': 'line', 'data': [], 'smooth': True, 'itemStyle': {'color': '#34d399'}, 'areaStyle': {'color': 'rgba(52, 211, 153, 0.2)'}}],
            'tooltip': {'trigger': 'axis'},
        }).classes('w-full h-64')

# --- Update Logic ---
# Store initial network state to calculate total bytes
net_io_start = psutil.net_io_counters()

def update_dashboard():
    global net_io_start
    now = datetime.now()
    
    # Update clock
    clock_label.set_text(now.strftime('%H:%M:%S'))
    
    # Update CPU
    cpu_percent = psutil.cpu_percent()
    cpu_ring.set_value(cpu_percent)
    
    # Update RAM
    ram = psutil.virtual_memory()
    ram_ring.set_value(ram.percent)
    ram_text.set_text(f'{ram.used / (1024**3):.1f} GB / {ram.total / (1024**3):.1f} GB')
    
    # Update Network Traffic
    net_io_current = psutil.net_io_counters()
    net_recv_label.set_text(f'{net_io_current.bytes_recv / (1024**2):.2f} MB')
    net_sent_label.set_text(f'{net_io_current.bytes_sent / (1024**2):.2f} MB')
    
    # Update Chart History
    time_str = now.strftime('%H:%M:%S')
    time_history.append(time_str)
    cpu_history.append(cpu_percent)
    
    # Keep only the last 20 data points
    if len(time_history) > 20:
        time_history.pop(0)
        cpu_history.pop(0)
        
    # Apply new data to the chart
    cpu_chart.options['xAxis']['data'] = time_history
    cpu_chart.options['series'][0]['data'] = cpu_history
    cpu_chart.update()

# Run the update function every 1 second
ui.timer(1.0, update_dashboard)

# Start the server
ui.run(title='IT Ops Dashboard', port=8080, show=False)