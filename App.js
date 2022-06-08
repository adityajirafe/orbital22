import { StatusBar } from 'expo-status-bar';
import * as Font from 'expo-font';
import * as SplashScreen from 'expo-splash-screen';
import React, { useState, useEffect, useCallback, Component } from 'react';
import { View, LogBox } from 'react-native';

import AppNavigator from './src/navigation/AppNavigator';
import { globalStyles } from './src/styles/Styles';

LogBox.ignoreLogs(['Warning: ...']); // Ignore log notification by message
LogBox.ignoreAllLogs(); //Ignore all log notifications


export default App = () => {
  
  const [appIsReady, setAppIsReady] = useState(false);

  useEffect(() => {
    async function prepare() {
      try {
        // Keep the splash screen visible while we fetch resources
        await SplashScreen.preventAutoHideAsync();
        // Pre-load fonts, make any API calls you need to do here
        await Font.loadAsync({
          'roboto' : require('./assets/fonts/RobotoMono.ttf'),
          'roboto-bold' : require('./assets/fonts/RobotoMono-Bold.ttf'),
          'advent': require('./assets/fonts/AdventPro-Bold.ttf')
        });
      } catch (e) {
        console.warn(e);
      } finally {
        // Tell the application to render
        setAppIsReady(true);
      }
    }
    prepare();
  }, []);

  const onLayoutRootView = useCallback(async () => {
    if (appIsReady) {
      // This tells the splash screen to hide immediately! If we call this after
      // `setAppIsReady`, then we may see a blank screen while the app is
      // loading its initial state and rendering its first pixels. So instead,
      // we hide the splash screen once we know the root view has already
      // performed layout.
      await SplashScreen.hideAsync();
    }
  }, [appIsReady]);

  if (!appIsReady) {
    return null;
  }

  return (
    <View 
      style={globalStyles.container}
      onLayout={onLayoutRootView}
      >
      <AppNavigator />
      <StatusBar style="auto" />
    </View>
  );
}