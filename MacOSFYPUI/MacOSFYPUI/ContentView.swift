//
//  ContentView.swift
//  MacOSFYPUI
//
//  This file is the UI itself. It is using SwiftUI and calls the Logic class, which is later passing the information to and from the Python backend
// 
//  Created by <><><><><><> on 30/11/2020.
//

import SwiftUI

// CONSTANTS
let textInputPlaceholder:String = "Enter your references here ..."
let textOutputPlaceholder:String = "Your recommendations will be printed here ..."


//CONTENT VIEW ITSELF
struct ContentView: View {
    @State private var textInput = ""
    @State private var isImporting = false
    @State private var filePath = "Default File"
    @State private var bestNPapers = 10
    @State private var output = ""
    @State private var methodSelection = 1
    
    let logic = Logic()
    
    @State var thorEnabled: Bool = false
    var body: some View {
        HStack {
            VStack {
                ZStack(alignment: .topLeading){
                    TextEditor(text: $textInput)
                        .foregroundColor(.primary)
                        .padding(0)
                    if (textInput == ""){
                        Text(textInputPlaceholder)
                            .foregroundColor(.gray)
                            .padding(.leading, 5)
                    }
                }
                Divider()
                ZStack(alignment: .topLeading){
                    TextEditor(text: $output)
                        .foregroundColor(.primary)
                        .padding(0)
                    if (output == ""){
                        Text(textOutputPlaceholder)
                            .foregroundColor(.gray)
                            .padding(.leading, 5)
                    }
                }
            }
            Divider()
            VStack {
                Toggle(isOn: $thorEnabled) {
                    Text("Thor Enabled")
                }
                Picker(selection: .constant(1), label: Text("Number of threads:")) {
                    ForEach((1...5), id: \.self) {
                        Text(String($0)).tag($0)
                    }
                }
            
                Button(action: {
                    print("collecting the data")
                    logic.saveCitationsToFile(citations: textInput)
                    logic.scrapeGoogle(threads: 1, thorEnabled: false)
                    
                }) {
                    Text("Collect the data")
                }
                
                Divider()
                
                HStack{
                    Text(filePath)
                    Button(action: {
                        isImporting = true
                    }){
                        Text("Find Custom File")
                    }
                    
                    Button(action: {
                        filePath = "Default File"
                    }){
                        Text("Clear")
                    }
                }

                HStack{
                    Text("Show only best papers:")
                    Stepper(value: $bestNPapers, in: (1...20)) {
                        Text("\(bestNPapers)")
                        }
                }
                
                Picker(selection: $methodSelection, label: Text("Method used:")) {
                    Text("Jaccard Similarity").tag(1)
                    Text("Jaccard Similarity Without devision").tag(2)
                    Text("Network Analysis Degree Centrality").tag(3)
                    Text("Network Analysis Betweenness Centrality").tag(4)
                }
                
                Button(action: {
                    print("analysing")
                    logic.analyseFile(filePath: filePath, bestNumber: bestNPapers, method: methodSelection)
                    let out = logic.readOutput()
                    print(out)
                    output = out
                    
                }) {
                    Text("Analyze the file")
                }
            }.padding(5)
            
        }.fileImporter(
            isPresented: $isImporting,
            allowedContentTypes: [.plainText],
            allowsMultipleSelection: false
        ) { result in
            do {
                guard let selectedFile: URL = try result.get().first else { return }
                isImporting = false
                filePath = String(selectedFile
                                    .absoluteString
                                    .dropFirst(7))
            } catch {
            }
        }
    }}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
            .padding()
    }
}
