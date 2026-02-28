//
//  ContentView.swift
//  AnyAlert
//
//  Created by derek klass on 3/22/21.
//

import SwiftUI

struct ContentView: View {
    var body: some View {
        Text("Hello Swift")
            .font(.largeTitle)
            .fontWeight(.light)
            .foregroundColor(Color.blue)
            .multilineTextAlignment(.leading)
            .frame(width: /*@START_MENU_TOKEN@*/100.0/*@END_MENU_TOKEN@*/, height: /*@START_MENU_TOKEN@*/100.0/*@END_MENU_TOKEN@*/)
            
            
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
