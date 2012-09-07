/* 
Copyright 2012 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "BSD" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/bsd_license
*/

#import <Cocoa/Cocoa.h>
#import "PyMoneyGuruApp.h"
#import "HSAboutBox.h"

@interface MGAppDelegate : NSObject
{
    NSWindow *preferencesPanel;
    NSTextField *autoSaveIntervalField;
    NSButton *autoDecimalPlaceButton;
    IBOutlet NSMenuItem *customDateRangeItem1;
    IBOutlet NSMenuItem *customDateRangeItem2;
    IBOutlet NSMenuItem *customDateRangeItem3;
    
    NSInvocation *continueUpdate;
    PyMoneyGuruApp *model;
    HSAboutBox *_aboutBox;
}

@property (readwrite, retain) NSWindow *preferencesPanel;
@property (readwrite, retain) NSTextField *autoSaveIntervalField;
@property (readwrite, retain) NSButton *autoDecimalPlaceButton;

- (PyMoneyGuruApp *)model;

- (IBAction)openExampleDocument:(id)sender;
- (IBAction)openWebsite:(id)sender;
- (IBAction)openHelp:(id)sender;
- (IBAction)openPluginFolder:(id)sender;
- (IBAction)showAboutBox:(id)sender;
- (IBAction)showPreferencesPanel:(id)sender;

- (void)setCustomDateRangeName:(NSString *)aName atSlot:(NSInteger)aSlot;

/* model --> view */
- (void)setupAsRegistered;
- (void)showFairwareNagWithPrompt:(NSString *)prompt;
- (void)showDemoNagWithPrompt:(NSString *)prompt;
- (void)showMessage:(NSString *)msg;
@end
