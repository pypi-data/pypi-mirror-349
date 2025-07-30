use std::num::NonZero;

use clap::{Parser, ValueEnum};

#[derive(Parser)]
struct Args {
    /// 読みの最大長。
    #[clap(short, long)]
    max_length: Option<NonZero<usize>>,

    /// アルゴリズム。
    #[clap(short, long, default_value = "greedy")]
    strategy: StrategyArg,

    /// Top-KのK。
    #[clap(short = 'k', long, default_value = "3")]
    top_k: usize,

    /// Top-PのP。
    #[clap(short = 'p', long, default_value = "0.9")]
    top_p: f32,

    /// Top-Pの温度。
    #[clap(short = 't', long, default_value = "1.0")]
    temperature: f32,
}

#[derive(ValueEnum, Debug, Clone)]
enum StrategyArg {
    Greedy,
    TopK,
    TopP,
}

fn main() {
    let args = Args::parse();

    let strategy = match args.strategy {
        StrategyArg::Greedy => {
            println!("アルゴリズム：Greedy");
            kanalizer::Strategy::Greedy
        }
        StrategyArg::TopK => {
            println!("アルゴリズム：Top-K, K={}", args.top_k);
            kanalizer::Strategy::TopK(kanalizer::StrategyTopK { k: args.top_k })
        }
        StrategyArg::TopP => {
            println!(
                "アルゴリズム：Top-P, P={}, T={}",
                args.top_p, args.temperature
            );
            kanalizer::Strategy::TopP(kanalizer::StrategyTopP {
                top_p: args.top_p,
                temperature: args.temperature,
            })
        }
    };

    println!("Ctrl-C で終了します。");
    loop {
        let line = dialoguer::Input::<String>::new()
            .with_prompt("Input")
            .interact()
            .unwrap();
        match kanalizer::convert(&line)
            .with_max_length(match args.max_length {
                Some(length) => length.into(),
                None => kanalizer::MaxLength::Auto,
            })
            .with_strategy(&strategy)
            .perform()
        {
            Ok(dst) => {
                println!("{line} -> {dst}");
            }
            Err(e) => {
                eprintln!("Error: {e}");
            }
        }
    }
}
