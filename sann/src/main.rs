#![recursion_limit = "256"]

mod file_io;
mod graph;
mod linalg_helpers;
mod my_gui;
mod renderer;
mod shared_shit;
mod simulated_annealing;
mod simulated_annealing_dumber_and_better;
mod stitcher;
mod types;

extern crate float_cmp;
extern crate glutin_window;
extern crate graphics;
extern crate opengl_graphics;
extern crate pathfinding;
extern crate piston;
extern crate rand;
extern crate toml;
extern crate vec1;

extern crate conrod_core;
extern crate conrod_piston;
extern crate find_folder;
extern crate geo;
extern crate num_traits;
extern crate piston_window;
extern crate regex;

use renderer::draw_mode::draw_mode_rendering;
use std::env;
use simulated_annealing::energy;
use graph::area;
use graph::types::OUTER;
use file_io::recorders;
use toml::from_str;
use graph::convex_hull::convex_hull_from_graph;

use num_traits::Pow;

extern crate csv;

use std::error::Error;
use std::io;
use csv::Writer;
use std::fs::File;
use std::io::prelude::*;

extern crate lexical;

fn real_main() {
    let params: types::Params = match std::fs::read_to_string("parameters.toml") {
        Err(_) => panic!("No parameters.toml file found in directory"),
        Ok(content) => file_io::toml_table_to_params(content.parse::<toml::Value>().unwrap()),
    };
    let (mut renderer, mut window) = renderer::setup_renderer();
    let mut sim_state = simulated_annealing::SimState::initial_state(&params);

    renderer::setup_optimization_and_loop(
        &mut sim_state,
        &mut window,
        &mut renderer,
        |ss| renderer::lines_from_thick_surface(&ss.ts),
        &params,
    )
}

fn no_gui_main(params_file_path: &str
    , how_many_reps: u64) 
    
    {
    
    let params: types::Params = match std::fs::read_to_string(params_file_path) {
        Err(_) => panic!(format!("Parameter file named \"{}\" not found.", params_file_path)),
        Ok(content) => file_io::toml_table_to_params(content.parse::<toml::Value>().unwrap()),
    };
    
   
    let mut recording_state = recorders::RecordingState::initial_state(&params).unwrap_or_else(|| {panic!("Couldn't create recording state")});
    let mut sim_state = simulated_annealing::SimState::initial_state(&params);
        
    loop {
        simulated_annealing_dumber_and_better::step(&mut sim_state, &params);
        
        if sim_state.timestep % 1000000 == 0 {
        
        println!(
"OUTER = {:?}
INNER = {:?}
EXP = {:?} ",graph::graph_to_points(&sim_state.ts.layers[0]),
 graph::graph_to_points(&sim_state.ts.layers[1]),
 graph::graph_to_points(&convex_hull_from_graph(&sim_state.ts.layers[0]))
 );
    

  
  	
    
            recorders::record(&sim_state, &params, &mut recording_state);
        
        }
        
        
        
        
        
        
        if sim_state.timestep == how_many_reps { // Não sei de onde tirar esse número
       
println!(
"OUTER = {:?}
INNER = {:?}
EXP = {:?} ",graph::graph_to_points(&sim_state.ts.layers[0]),
 graph::graph_to_points(&sim_state.ts.layers[1]),
 graph::graph_to_points(&convex_hull_from_graph(&sim_state.ts.layers[0]))
 );
    

  
  	
    
            recorders::record(&sim_state, &params, &mut recording_state);
               
            break;            
        	}
        
        }
        
    }


fn create_csv_out(matrix: Vec<(f64, f64)>, output: &str) -> Result<(), Box<dyn Error>> {

    let file_path = format!("{}/dados_out.csv",output);
    let mut file = File::create(file_path)?;

    // Escrever cabeçalho
    writeln!(file, "Componente1,Componente2")?;

    // Escrever dados da matriz
    for (comp1, comp2) in matrix {
        writeln!(file, "{},{}", comp1, comp2)?;
    }

    println!("Arquivo CSV gerado com sucesso!");

    Ok(())
}

fn create_csv_in(matrix: Vec<(f64, f64)>, output: &str) -> Result<(), Box<dyn Error>> {
    
    let file_path = format!("{}/dados_in.csv",output);
    let mut file = File::create(file_path)?;

    // Escrever cabeçalho
    writeln!(file, "Componente1,Componente2")?;

    // Escrever dados da matriz
    for (comp1, comp2) in matrix {
        writeln!(file, "{},{}", comp1, comp2)?;
    }

    println!("Arquivo CSV gerado com sucesso!");

    Ok(())
}

fn create_csv_ext(matrix: Vec<(f64, f64)>, output: &str) -> Result<(), Box<dyn Error>> {

    let file_path = format!("{}/dados_ext.csv", output);
    let mut file = File::create(file_path)?;


    // Escrever cabeçalho
    writeln!(file, "Componente1,Componente2")?;

    // Escrever dados da matriz
    for (comp1, comp2) in matrix {
        writeln!(file, "{},{}", comp1, comp2)?;
    }

    println!("Arquivo CSV gerado com sucesso!");

    Ok(())
}



fn coord_main(params_file_path: &str
    , how_many_reps: u64, output: &str) 
    
    {
    
    let params: types::Params = match std::fs::read_to_string(params_file_path) {
        Err(_) => panic!(format!("Parameter file named \"{}\" not found.", params_file_path)),
        Ok(content) => file_io::toml_table_to_params(content.parse::<toml::Value>().unwrap()),
    };
    
   
    let mut recording_state = recorders::RecordingState::initial_state(&params).unwrap_or_else(|| {panic!("Couldn't create recording state")});
    let mut sim_state = simulated_annealing::SimState::initial_state(&params);
    
    let mut sum_E = 0.0;
    let mut sum_E_2 = 0.0;
    
    let mut sum_K = 0.0;
    let mut sum_K_2 = 0.0;
    
        
    loop {
        simulated_annealing_dumber_and_better::step(&mut sim_state, &params);
        recorders::record(&sim_state, &params, &mut recording_state);
        
        let K = recorders::k(&sim_state.ts, &params);
        let E = recorders::energy(&sim_state.ts, &params);
        let t = sim_state.timestep as f64;
        
        sum_E += E;
        let media_E = sum_E/t;
        let E_2 = (E - media_E)*(E - media_E);        
        sum_E_2 += E_2 ;
        let var_E = E_2/t;
        
        sum_K += K;
        let media = sum_K/t;
        let K_2 = (K - media)*(K - media);        
        sum_K_2 += K_2 ;
        let var = K_2/t;
        
        
        if sim_state.timestep % 100 == 0 {
        println!("step: {:?}",sim_state.timestep);
        
        println!("step: {:?}",var);
        
        println!("step: {:?}",var_E);
        
        
        
        }
        
        if sim_state.timestep == how_many_reps { // Não sei de onde tirar esse número
    let matrix_out = graph::graph_to_points(&sim_state.ts.layers[0]);
    let matrix_in = graph::graph_to_points(&sim_state.ts.layers[1]);
    let matrix_ext = graph::graph_to_points(&convex_hull_from_graph(&sim_state.ts.layers[0]));

    // Chamar a função para criar o arquivo CSV
    if let Err(err) = create_csv_out(matrix_out,output) {
        eprintln!("Erro ao criar o arquivo CSV: {}", err);
    }	
    if let Err(err) = create_csv_in(matrix_in,output) {
        eprintln!("Erro ao criar o arquivo CSV: {}", err);
    }			
    if let Err(err) = create_csv_ext(matrix_ext,output) {
        eprintln!("Erro ao criar o arquivo CSV: {}", err);
    }			
            recorders::record(&sim_state, &params, &mut recording_state);
        
        break;            
        	}
        
        if sim_state.timestep % 1000 == 0 {
        
        
    

  
  		
    
    let matrix_out = graph::graph_to_points(&sim_state.ts.layers[0]);
    let matrix_in = graph::graph_to_points(&sim_state.ts.layers[1]);
    let matrix_ext = graph::graph_to_points(&convex_hull_from_graph(&sim_state.ts.layers[0]));

    // Chamar a função para criar o arquivo CSV
    if let Err(err) = create_csv_out(matrix_out,output) {
        eprintln!("Erro ao criar o arquivo CSV: {}", err);
    }	
    if let Err(err) = create_csv_in(matrix_in,output) {
        eprintln!("Erro ao criar o arquivo CSV: {}", err);
    }			
    if let Err(err) = create_csv_ext(matrix_ext,output) {
        eprintln!("Erro ao criar o arquivo CSV: {}", err);
    }			
            recorders::record(&sim_state, &params, &mut recording_state);
        
        }
        
        
        
        
        
        if var > 0.0{
        if var <= f64::pow(10.0,-10) { 
        // Não sei de onde tirar esse número
        let matrix_out = graph::graph_to_points(&sim_state.ts.layers[0]);
        let matrix_in = graph::graph_to_points(&sim_state.ts.layers[1]);
        let matrix_ext = graph::graph_to_points(&convex_hull_from_graph(&sim_state.ts.layers[0]));

    // Chamar a função para criar o arquivo CSV
    if let Err(err) = create_csv_out(matrix_out,output) {
        eprintln!("Erro ao criar o arquivo CSV: {}", err);
    }	
    if let Err(err) = create_csv_in(matrix_in,output) {
        eprintln!("Erro ao criar o arquivo CSV: {}", err);
    }			
    if let Err(err) = create_csv_ext(matrix_ext,output) {
        eprintln!("Erro ao criar o arquivo CSV: {}", err);
    }			
            recorders::record(&sim_state, &params, &mut recording_state);
            
        

               
                        
        	}
        }
        }
        
    }

fn media(x: &f64, t: &f64) -> f64 {
    x/t
}



fn playin_main() {
    let (mut renderer, mut window) = renderer::setup_renderer();
    draw_mode_rendering(&mut window, &mut renderer)
}

fn main() {
    let args: Vec<String> = env::args().collect();
    let empty_vec: Vec<i64> = Vec::new();
    let s: Vec<i64> = empty_vec.iter().map(|x| *x).collect();
    if args.len() < 2 {
        real_main()
    } else if args[1] == "debug" {
        playin_main()
    } else if args[1] == "smart" {
        println!("Path hehe: djumba");
    } else if args[1] == "conrod" {
        shared_shit::conrod_main();
    } else if args[1] == "my_gui" {
        my_gui::my_ui_main();
    } else if args[1] == "no_gui" {
        no_gui_main(&args[2], args[3].parse::<u64>().unwrap());
    } else if args[1] == "coord" {
        coord_main(&args[2], args[3].parse::<u64>().unwrap(),&args[4]);
    }
}
