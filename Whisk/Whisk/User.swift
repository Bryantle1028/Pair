//
//  User.swift
//  Whisk
//
//  Created by Wade Rance on 2/10/19.
//  Copyright © 2019 BryantLe. All rights reserved.
//

import UIKit

class User {
    // MARK: Properties
    
    var firstName: String
    var lastName: String
    var location: [Double]
    var radius: Int
    var gender: Bool
    var preference: [Bool]
    var photos: [UIImage]
    // var vector: VECTOR CLASS
    
    // MARK: Initialization
    
    init?(name: String, photo: UIImage?, rating: Int) {
        // The name must not be empty
        guard !name.isEmpty else {
            return nil
        }
        
        // The rating must be between 0 and 5 inclusively
        guard (rating >= 0) && (rating <= 5) else {
            return nil
        }
        
        self.name = name
        self.photo = photo
        self.rating = rating

    }
}
