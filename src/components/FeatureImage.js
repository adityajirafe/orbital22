import { StyleSheet, Image, View } from 'react-native';
import React from 'react';

const FeatureImage = props => {

    return (
        <View style = {styles.image_container}>
            <Image 
                source = {require('../../assets/images/coinValet_home.jpeg')}
                style = {styles.image} />
        </View>
    );
};

export default FeatureImage;

const styles = StyleSheet.create({
    image: {
        width: '100%',
        height: '100%',
        resizeMode: 'contain'
    },
    image_container: {
        flex: 1,
    },
});
