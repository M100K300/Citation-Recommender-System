//
//  Logic.swift
//  MacOSFYPUI
//  This class contains all the logic connecting the UI to the Python back end.
//
//  Created by <><><><><><> on 17/02/2021.
//

import Foundation


class Logic {
    
    func analyseFile(filePath: String, bestNumber: Int, method: Int){
                    let task = Process()
                    task.executableURL = URL(fileURLWithPath: "/usr/local/bin/python3") // change if python instalation is different

                    var methodName = ""
                    if method == 1{
                        methodName = "jaccard"
                    } else if method == 2{
                        methodName = "jaccard_no_division"
                    } else if method ==  3{
                        methodName = "network_degree"
                    }else {
                        methodName  = "network_betweenness"
                    }
                    
        let inputFile = filePath == "Default File" ? String("\(self.getDocDir().appendingPathComponent("data_collection_output.csv"))".dropFirst(7)) : filePath
                    
                    let outputFilename = "\(self.getDocDir().appendingPathComponent("final_output.csv"))".dropFirst(7)
                    
                    let analystFilename = "\(self.getDocDir().appendingPathComponent("RecommenderSystem/analysis.py"))".dropFirst(7)
                    
                    
                    task.arguments = [  String(analystFilename),
                                        "-m", "\(methodName)",
                                        "-i", "\(inputFile)",
                                        "-o", String(outputFilename),
                                        "-n", "\(bestNumber)"]
                    
                    let pipe = Pipe()
                    task.standardOutput = pipe
                    task.launch()
            print("executing")
                    let data = pipe.fileHandleForReading.readDataToEndOfFile()
                    print("output analysis: \(NSString(data: data, encoding: String.Encoding.utf8.rawValue) ?? "no-output")")
        
    }
    
    
    private func getDocDir() -> URL {
        return FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0]
    }
    
    func readOutput() -> String{
        let filename = "\(getDocDir().appendingPathComponent("final_output.csv"))".dropFirst(7)
        var toReturn = ""
        if freopen("\(filename)", "r", stdin) == nil {
            perror("\(filename)")
        }
        while let line = readLine() {
            toReturn.append("\n\(line)")
        }
        return toReturn
    }
    
    func saveCitationsToFile(citations: String){
        
        let filename = getDocDir().appendingPathComponent( "data_collection_input.csv")
        do{
            try "\(citations)\n".write(to: filename, atomically: true, encoding: String.Encoding.utf8)
        }catch{
            print("error writing to the file \(error)")
        }
        
    }
    
    // input file is always going to be default
    func scrapeGoogle(threads: Int, thorEnabled: Bool){
        let task = Process()
        task.executableURL = URL(fileURLWithPath: "/usr/local/bin/python3")
        task.currentDirectoryURL = self.getDocDir()
        let inputFilename = "\(getDocDir().appendingPathComponent( "data_collection_input.csv"))".dropFirst(7)
        let outputFilename = "\(self.getDocDir().appendingPathComponent("data_collection_output.csv"))".dropFirst(7)
        let analystFilename = "\(self.getDocDir().appendingPathComponent("RecommenderSystem/scraper.py"))".dropFirst(7)

        if (thorEnabled) {
        task.arguments = [String(analystFilename),
                            "-i", "\(inputFilename)",
                            "-o", "\(outputFilename)",
                            "-n", "\(threads)",
                            "-t"]
        } else {
            task.arguments = [String(analystFilename),
                                "-i", "\(inputFilename)",
                                "-o", "\(outputFilename)",
                                "-n", "\(threads)"]
        }
        
        let pipe = Pipe()
        task.standardOutput = pipe
        task.launch()
        print("executing")
        let data = pipe.fileHandleForReading.readDataToEndOfFile()
        print("output analysis: \(NSString(data: data, encoding: String.Encoding.utf8.rawValue) ?? "no-output")")
    }
    
}
