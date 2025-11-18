/// Terminal User Interface (TUI)
/// 
/// Beautiful, colorized dashboard and interactive interface using Ratatui

use ratatui::{
    backend::Backend,
    Terminal,
    Frame,
    layout::{Layout, Constraint, Direction},
    widgets::{Block, Borders, Paragraph, Gauge, Sparkline, List, ListItem},
    style::{Color, Style, Modifier},
    text::{Line, Span},
};
use std::sync::Arc;
use parking_lot::Mutex;

pub struct TuiApp {
    pub state: Arc<Mutex<AppState>>,
}

#[derive(Clone)]
pub struct AppState {
    pub current_screen: Screen,
    pub generator_stats: GeneratorStats,
    pub logs: Vec<String>,
    pub selected_preset: Option<String>,
    pub running: bool,
}

#[derive(Clone, Debug)]
pub enum Screen {
    Dashboard,
    Presets,
    Generator,
    Monitor,
    Settings,
}

#[derive(Clone, Default)]
pub struct GeneratorStats {
    pub tokens_generated: u64,
    pub tokens_per_second: f64,
    pub uptime_seconds: u64,
    pub memory_usage_mb: u64,
    pub cpu_percent: f64,
}

impl TuiApp {
    pub fn new() -> Self {
        Self {
            state: Arc::new(Mutex::new(AppState {
                current_screen: Screen::Dashboard,
                generator_stats: GeneratorStats::default(),
                logs: vec![
                    "🚀 OmniWordlist Pro v1.1.0 initialized".to_string(),
                    "✓ Field catalog loaded (1500+ fields)".to_string(),
                    "✓ Transform engines ready".to_string(),
                    "Ready for wordlist generation!".to_string(),
                ],
                selected_preset: None,
                running: false,
            })),
        }
    }

    pub fn render(&self, frame: &mut Frame) {
        let state = self.state.lock();

        match state.current_screen {
            Screen::Dashboard => self.render_dashboard(frame, &state),
            Screen::Presets => self.render_presets(frame, &state),
            Screen::Generator => self.render_generator(frame, &state),
            Screen::Monitor => self.render_monitor(frame, &state),
            Screen::Settings => self.render_settings(frame, &state),
        }
    }

    fn render_dashboard(&self, frame: &mut Frame, state: &AppState) {
        let size = frame.size();

        let chunks = Layout::default()
            .direction(Direction::Vertical)
            .margin(1)
            .constraints([
                Constraint::Length(3),
                Constraint::Min(10),
                Constraint::Length(15),
            ])
            .split(size);

        // Header
        let header = Paragraph::new(
            vec![
                Line::from(vec![
                    Span::styled("🚀 OmniWordlist Pro v1.1.0", Style::default()
                        .fg(Color::Cyan)
                        .add_modifier(Modifier::BOLD)),
                    Span::raw(" | Enterprise Wordlist Generator"),
                ]),
                Line::from(vec![
                    Span::raw("━".repeat(size.width as usize - 2)),
                ]),
            ]
        ).block(Block::default().borders(Borders::NONE));

        frame.render_widget(header, chunks[0]);

        // Main content
        let content_chunks = Layout::default()
            .direction(Direction::Horizontal)
            .constraints([
                Constraint::Percentage(50),
                Constraint::Percentage(50),
            ])
            .split(chunks[1]);

        // Stats panel
        let stats_text = vec![
            Line::from(vec![Span::styled("📊 Statistics", Style::default()
                .fg(Color::Green)
                .add_modifier(Modifier::BOLD))]),
            Line::from(""),
            Line::from(vec![
                Span::raw("Tokens Generated: "),
                Span::styled(format!("{}", state.generator_stats.tokens_generated),
                    Style::default().fg(Color::Yellow)),
            ]),
            Line::from(vec![
                Span::raw("Rate: "),
                Span::styled(format!("{:.2} tok/s", state.generator_stats.tokens_per_second),
                    Style::default().fg(Color::Yellow)),
            ]),
            Line::from(vec![
                Span::raw("Memory: "),
                Span::styled(format!("{} MB", state.generator_stats.memory_usage_mb),
                    Style::default().fg(Color::Yellow)),
            ]),
            Line::from(vec![
                Span::raw("CPU: "),
                Span::styled(format!("{:.1}%", state.generator_stats.cpu_percent),
                    Style::default().fg(Color::Yellow)),
            ]),
            Line::from(""),
            Line::from(vec![Span::styled("Status: ", Style::default()
                .add_modifier(Modifier::DIM))]),
            if state.running {
                Line::from(vec![Span::styled("🔴 RUNNING", Style::default()
                    .fg(Color::Red)
                    .add_modifier(Modifier::BOLD))])
            } else {
                Line::from(vec![Span::styled("🟢 IDLE", Style::default()
                    .fg(Color::Green)
                    .add_modifier(Modifier::BOLD))])
            },
        ];

        let stats_block = Block::default()
            .title("  Stats  ")
            .borders(Borders::ALL)
            .border_type(ratatui::widgets::BorderType::Rounded)
            .style(Style::default().fg(Color::Cyan));

        let stats = Paragraph::new(stats_text)
            .block(stats_block)
            .style(Style::default().fg(Color::White));

        frame.render_widget(stats, content_chunks[0]);

        // Quick actions
        let actions_text = vec![
            Line::from(vec![Span::styled("⚡ Quick Actions", Style::default()
                .fg(Color::Magenta)
                .add_modifier(Modifier::BOLD))]),
            Line::from(""),
            Line::from(vec![
                Span::raw("  "),
                Span::styled("[1]", Style::default().fg(Color::Cyan)),
                Span::raw(" Dashboard"),
            ]),
            Line::from(vec![
                Span::raw("  "),
                Span::styled("[2]", Style::default().fg(Color::Cyan)),
                Span::raw(" Presets"),
            ]),
            Line::from(vec![
                Span::raw("  "),
                Span::styled("[3]", Style::default().fg(Color::Cyan)),
                Span::raw(" Generate"),
            ]),
            Line::from(vec![
                Span::raw("  "),
                Span::styled("[4]", Style::default().fg(Color::Cyan)),
                Span::raw(" Monitor"),
            ]),
            Line::from(vec![
                Span::raw("  "),
                Span::styled("[5]", Style::default().fg(Color::Cyan)),
                Span::raw(" Settings"),
            ]),
            Line::from(""),
            Line::from(vec![
                Span::raw("  "),
                Span::styled("[q]", Style::default().fg(Color::Red)),
                Span::raw(" Quit"),
            ]),
        ];

        let actions_block = Block::default()
            .title("  Navigation  ")
            .borders(Borders::ALL)
            .border_type(ratatui::widgets::BorderType::Rounded)
            .style(Style::default().fg(Color::Green));

        let actions = Paragraph::new(actions_text)
            .block(actions_block);

        frame.render_widget(actions, content_chunks[1]);

        // Logs panel
        let log_items: Vec<ListItem> = state.logs.iter()
            .rev()
            .take(10)
            .map(|log| {
                let style = if log.starts_with('✓') {
                    Style::default().fg(Color::Green)
                } else if log.starts_with('❌') {
                    Style::default().fg(Color::Red)
                } else if log.starts_with('⚠') {
                    Style::default().fg(Color::Yellow)
                } else {
                    Style::default().fg(Color::White)
                };

                ListItem::new(log.clone()).style(style)
            })
            .collect();

        let logs = List::new(log_items)
            .block(Block::default()
                .title("  Recent Events  ")
                .borders(Borders::ALL)
                .border_type(ratatui::widgets::BorderType::Rounded)
                .style(Style::default().fg(Color::Blue)));

        frame.render_widget(logs, chunks[2]);
    }

    fn render_presets(&self, _frame: &mut Frame, _state: &AppState) {
        // Placeholder
    }

    fn render_generator(&self, _frame: &mut Frame, _state: &AppState) {
        // Placeholder
    }

    fn render_monitor(&self, _frame: &mut Frame, _state: &AppState) {
        // Placeholder
    }

    fn render_settings(&self, _frame: &mut Frame, _state: &AppState) {
        // Placeholder
    }
}

/// ASCII art header
pub fn print_banner() {
    let banner = r#"
╔═══════════════════════════════════════════════════════════════════════╗
║                  🚀 OmniWordlist Pro v1.1.0 🚀                       ║
║        Enterprise-Grade Wordlist Generation Platform in Rust         ║
║                                                                       ║
║  ✓ Crunch-compatible pattern generation                             ║
║  ✓ CUPP-style personalization + 1500+ fields                        ║
║  ✓ 100+ advanced transforms (leet, homoglyph, emoji...)            ║
║  ✓ Streaming generation with checkpointing                          ║
║  ✓ Beautiful TUI with colors & ASCII art                            ║
║  ✓ S3/MinIO, RocksDB, SQLite storage                                ║
║                                                                       ║
║  Pentest. Research. Creative. All-in-one.                           ║
╚═══════════════════════════════════════════════════════════════════════╝
    "#;
    
    println!("{}", banner);
}

/// Simple progress bar
pub fn print_progress(current: u64, total: u64) {
    let percent = if total > 0 {
        (current as f64 / total as f64 * 100.0) as u32
    } else {
        0
    };

    let filled = percent / 5;
    let empty = 20 - filled;

    print!("\r[");
    print!("{}", "█".repeat(filled as usize));
    print!("{}", "░".repeat(empty as usize));
    print!("] {}% ({}/{})", percent, current, total);
    std::io::Write::flush(&mut std::io::stdout()).ok();
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_tui_creation() {
        let app = TuiApp::new();
        let state = app.state.lock();
        assert_eq!(state.logs.len(), 4);
    }
}
